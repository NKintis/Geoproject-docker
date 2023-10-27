# Geoproject-docker
### Getting Started
**Description**
This repository contains scripts and a Dockerfile for downloading and preprocessing Sentinel-2 satellite images. The provided Python scripts facilitate the extraction of specific bands, projection conversion, and creation of a Spatio-Temporal Asset Catalog (STAC) for the processed data.

**Key Features**
* Automated download of Sentinel-2 images
* Preprocessing steps for different bands and resolutions
* Generation of a STAC catalog for organized data management
* Compatible with Docker for easy deployment and reproducibility

**Download Docker.**

Docker Desktop for Windows:
```shell
curl -fsSL https://desktop.docker.com/win/stable/Docker%20Desktop%20Installer.exe -o DockerDesktopInstaller.exe
start DockerDesktopInstaller.exe
```

Docker Desktop for Mac (Apple):
```shell
curl -fsSL https://desktop.docker.com/mac/stable/Docker%20Desktop%20Installer.dmg -o DockerDesktopInstaller.dmg
hdiutil attach DockerDesktopInstaller.dmg
cp -R /Volumes/Docker\ Desktop/Docker\ Desktop.app /Applications
hdiutil detach /Volumes/Docker\ Desktop
```

Docker Engine for Linux:
```shell
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```
**Building and Running with Docker**

**To build and run the project using Docker, follow these steps:**

**1. Clone the repository and navigate to the geospatial_project_docker directory.:**
```shell
	git clone https://github.com/NKintis/geospatial_project_docker
	cd geospatial_project_docker
```

**2. Build the Docker image:**
```shell
docker build -t image1 .
```

**3. Run the Docker container:**
```shell
docker run -p 8888:8888 -e USERNAME= -e PASSWORD= -e VAR1= -e VAR2= -e VAR3= -e VAR4= -e VAR5= -e VAR6= image1
```

Fill the environment variables (USERNAME, PASSWORD, VAR1, etc.) with your desired values.
* VAR1=MINIMUM_LONGITUDE 
* VAR2=MINIMUM_LATITUDE 
* VAR3=MAXIMUM_LONGITUDE
* VAR4=MAXIMUM_LATITUDE
* VAR5=START_DATE
* VAR6=END_DATE

Example:
```shell
docker run -p 8893:8888 -e USERNAME=nkintis -e PASSWORD=Nikos1234 -e VAR1=22.792511 -e VAR2=38.462192 -e VAR3=23.041077 -e VAR4=38.550313 -e VAR5=2018-01-01 -e VAR6=2018-01-02 image1
```

### Accessing JupyterLab

Open the link provided after running the container to access the processed data on Jupyterlab.

