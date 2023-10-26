import os

# Define input and output paths
internal_input_path = '/sample_data/raw'
internal_output_path = '/app/processed_data'
failures = []

# Loop through products in the input path
for product in os.listdir(internal_input_path):
    # Create output directory
    out_dir = internal_output_path
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    # Extract tile ID from the product name
    out_dir = os.path.join(out_dir, product.split('_')[5][1:])
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    path = os.path.join(internal_input_path, product)

    # Find the workspace (ws)
    for catalogue_product in os.listdir(os.path.join(path, 'GRANULE')):
        ws = os.path.join(path, 'GRANULE', catalogue_product, 'IMG_DATA')
        break

  
    try:
        # Extract year, month, and day from the product name
        month = product.split('_')[2][4:6]
        day = product.split('_')[2][6:8]
        year = product.split('_')[2][:4]
        out_dir_year = os.path.join(out_dir, year)
        if not os.path.exists(out_dir_year):
            os.mkdir(out_dir_year)

        out_dir_final = os.path.join(out_dir_year, month)
        if not os.path.exists(out_dir_final):
            os.mkdir(out_dir_final)
        out_dir_final = os.path.join(out_dir_year, month, day)
        if not os.path.exists(out_dir_final):
            os.mkdir(out_dir_final)

        # Process bands in R60m
        for band in os.listdir(os.path.join(ws, 'R60m')):
            if not 'B09' in band:
                continue
            new_product = os.path.join(out_dir_final, band.split('_60m')[0] + '.tif')
            if os.path.exists(new_product):
                continue
            product_path = os.path.join(ws, 'R60m', band)
            os.system('gdalwarp -t_srs EPSG:3857 -co COMPRESS=DEFLATE -co TILED=True -co PREDICTOR=2 -co NUM_THREADS=ALL_CPUS -tr 10 10 %s %s' % (product_path, new_product))
            break

        # Process bands in R10m
        for band in os.listdir(os.path.join(ws, 'R10m')):
            if 'B02' in band or 'B03' in band or 'B04' in band or 'B08' in band or 'TCI' in band:
                new_product = os.path.join(out_dir_final, band.split('_10m')[0] + '.tif')
                if os.path.exists(new_product):
                    continue
                product_path = os.path.join(ws, 'R10m', band)
                os.system('gdalwarp -t_srs EPSG:3857 -co COMPRESS=DEFLATE -co TILED=True -co PREDICTOR=2 -co NUM_THREADS=ALL_CPUS -tr 10 10 %s %s' % (product_path, new_product))

        # Process bands in R20m
        for band in os.listdir(os.path.join(ws, 'R20m')):
            if 'B02' in band or 'B03' in band or 'B04' in band or 'B08' in band or 'TCI' in band or 'AOT' in band or 'WVP' in band:
                continue
            else:
                new_product = os.path.join(out_dir_final, band.split('_20m')[0] + '.tif')
                if os.path.exists(new_product):
                    continue
                product_path = os.path.join(ws, 'R20m', band)
                os.system('gdalwarp -t_srs EPSG:3857 -co COMPRESS=DEFLATE -co TILED=True -co PREDICTOR=2 -co NUM_THREADS=ALL_CPUS -tr 10 10 %s %s' % (product_path, new_product))

    except Exception as e:
        print(e)
        failures.append(e)


print("Failures:", failures)


print("Starting creating the STAC catalogue")

import glob
import os
import fnmatch
import pystac
import rasterio
from pystac.extensions.eo import EOExtension
from shapely.geometry import Polygon, mapping
from datetime import datetime, timezone

# Function to get bounding box and footprint from a raster file
def get_bbox_and_footprint(raster):
    with rasterio.open(raster) as r:
        bounds = r.bounds
        bbox = [bounds.left, bounds.bottom, bounds.right, bounds.top]
        footprint = Polygon([
            [bounds.left, bounds.bottom],
            [bounds.left, bounds.top],
            [bounds.right, bounds.top],
            [bounds.right, bounds.bottom]
        ])

        return (bbox, mapping(footprint))

# Create a new STAC catalog
catalog = pystac.Catalog(id="s2-catalog", description='This catalog is a basic demonstration catalog utilizing sentinel-2 scenes.')

# Set the workspace path
ws = 'processed_data'

# Initialize a dictionary for tiles
tiles = {}

# Recursively search for files in the workspace
for dirpath, dirnames, files in os.walk(ws):
    for f in fnmatch.filter(files, '*.tif'):
        # Process only if 'B04' is in the file name
        if 'B04' not in f:
            continue
        tile = f[1:5]
        sensing_date = f[7:15]
        tif_path = os.path.join(dirpath, f)
        bbox, footprint = get_bbox_and_footprint(tif_path)
        date_format = "%Y%m%d"
        datetime_utc = datetime.strptime(sensing_date, date_format)

        # Create a new STAC item
        item = pystac.Item(id=tile+'_'+sensing_date,
                  geometry=footprint,
                  bbox=bbox,
                  datetime=datetime_utc,
                  properties={})

        # Define a list of bands
        bands = ['B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B8A', 'B09', 'B10', 'B11', 'B12', 'SCL', 'TCI']

        for band in bands:
            band_path = os.path.join(dirpath, f.replace('B04', band))
            if os.path.exists(band_path):
                item.add_asset(band, pystac.Asset(href=band_path, media_type='image/tiff'))
            else:
                print(f"Warning: Band {band} not found for item {item.id}")

        # Add EO extension to the item
        eo_ext = EOExtension.ext(item, add_if_missing=True)

        # Add the item to the catalog
        catalog.add_item(item)

# Print information about the items in the catalog
for item in catalog.get_all_items():
    print(f"Item ID: {item.id}")

    # Check if the item has assets
    if item.assets:
        # Print the assets of the item
        for asset_key, asset in item.assets.items():
            print(f"  Asset key: {asset_key}")
            print(f"  Asset href: {asset.href}")
            print(f"  Asset media type: {asset.media_type}")
            print(f"  Asset title: {asset.title}")
            print(f"  Asset description: {asset.description}")
            print("  ---")
    else:
        print("No assets for this item.")

    print("===")

# Normalize hrefs and save the catalog
catalog.normalize_hrefs(os.path.join('processed_data', "stac"))
catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)


