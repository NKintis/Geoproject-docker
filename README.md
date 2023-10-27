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
