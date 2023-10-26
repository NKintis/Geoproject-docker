import os
import zipfile
import sys
import docker
# Get environment variables
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')

# Get float variables from environment variables
var1 = float(os.environ.get('VAR1'))
var2 = float(os.environ.get('VAR2'))
var3 = float(os.environ.get('VAR3'))
var4 = float(os.environ.get('VAR4'))

# Get string variables from environment variables
var5 = os.environ.get('VAR5')
var6 = os.environ.get('VAR6')

# Create a bounding box list
bbox = [var1, var2, var3, var4]

# Set start and end dates
start_date = var5
end_date = var6

# Initialize HDA Client
from hda import Client, Configuration
from pathlib import Path
import sys
import docker
import subprocess
conf = Configuration(user=username, password=password)
hda_client = Client(config=conf)

# Check if hdarc file exists, if not create it
hdarc = Path(Path.home() / '.hdarc')
if not hdarc.is_file():
    import getpass
    with open(Path.home() / '.hdarc', 'w') as f:
        f.write(f'user:{username}\n')
        f.write(f'password:{password}\n')

# Define the search query
query = {
    "datasetId": "EO:ESA:DAT:SENTINEL-2:MSI",
    "boundingBoxValues": [
        {
            "name": "bbox",
            "bbox": bbox
        }
    ],
    "dateRangeSelectValues": [
        {
            "name": "position",
            "start": f"{start_date}T00:00:00.000Z",
            "end": f"{end_date}T00:00:00.000Z"
        }
    ],
    "stringChoiceValues": [
        {
            "name": "processingLevel",
            "value": "S2MSI2A"
        }
    ],
    "stringInputValues": [
        {
            "name": "cloudCover",
            "value": "70"
        }
    ]
}
try:
# Search for matching products
 print("Mpanei try")
 matches = hda_client.search(query)
except Exception as e:
    # Handle the exception
    print("Mpanei except")
    with open('/shared_files/error_message.txt', 'w') as error_file:
        error_file.write("ERROR")
    subprocess.run(['docker', 'stop', os.getenv('HOSTNAME')])
   
# Download the matching products
print("Bgike apo try")
matches.download(download_dir="/sample_data/raw")

# Get the list of downloaded files
downloaded_files = matches[0].results

#matches = hda_client.search(query)

# Define the directory for extraction
extracted_dir = '/sample_data/raw'

# Loop through the downloaded files and extract them
for product in os.listdir(extracted_dir):
    print(product)
    zip_path = os.path.join(extracted_dir, product)
    os.system(f"unzip {zip_path} -d {extracted_dir}")
    print(f'Contents from {product} extracted to {extracted_dir}')
    os.remove(zip_path)  # Remove the zip file after extraction

