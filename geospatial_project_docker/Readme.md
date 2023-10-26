### Getting Started

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
sudo docker build -t image1 .
```



