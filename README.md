# AGILE2023-reproduction
This repository is here to do the reproduction of the article "Cycling network evolution in OpenStreetMap" published at AGILE 2023 conference

The requirements section presents what tools are needed in order to reproduce the experiments. The data download part leads to the website where the data was downloaded. The network generation part explains how to create a network from the downloaded data.

#Requirements

The experience has been done with Ubuntu 20. The following subsections describe the installation process specifically for this operating system.

##OSRM
The first step consist in installing OSRM. The link here can help for the installation of OSRM (https://www.linuxbabe.com/ubuntu/install-osrm-ubuntu-20-04-open-source-routing-machine, only steps 1 and 2).

##Python 3.8

You can download Python by using this link (https://techpiezo.com/python/install-python-3-8-3-in-ubuntu-20-04-lts/) or use a specific environment with Python 3.8.
The following packages should also be installed. Since pip is installed with Python 3.8, you just have to launch the following instructions:
- numpy (pip install numpy)
- requests (pip install requests)
- geoson (pip install geojson)
- csv (pip install csv)

##R 4.1
This link explains how to install R for our operating system (https://linuxize.com/post/how-to-install-r-on-ubuntu-20-04/)

##QGIS 3.*
Follow this link to install QGIS (https://www.qgis.org/en/site/forusers/alldownloads.html#linux)

#Data download

The data used for the experiment is here (TODO).
If you want to use data on another region, create an OpenStreetMap account and go to https://osm-internal.download.geofabrik.de/. At the bottom of the page, in the yellow area, click on connect with your OpenStreetMap account and choose the area you want.

#Network generation

Here is an example for the 2014 snapshot in Centre Val-de-Loire region. Repeat it for every network you want.
The following instructions create a cycling network based on our data extracted from Geofabrik.
cd working/directory
docker run -t -v "${PWD}:/path/to/store/data/2014" osrm/osrm-backend osrm-extract -p /opt/bicycle.lua /path/to/data/centre2014.osm.pbf

sudo docker run -t -v "${PWD}:/path/to/store/data/2014" osrm/osrm-backend osrm-partition /path/to/data/centre2014.osrm

sudo docker run -t -v "${PWD}:/path/to/store/data/2014" osrm/osrm-backend osrm-customize /path/to/data/centre2014.osrm

#Route generation

You first need to turn the services on. The parameter 5014 should be changed for each network if you want to run multiple networks at the same time.

sudo docker run -d -p 5014:5000 -v "/path/to/store/data:/data" osrm/osrm-backend osrm-routed --algorithm mld /path/to/data/centre2014.osrm

You can now launch the Python script to generate the routes. If you have chosen another area, you should change the bounding box in the script. The results are two files named alldataZones.geojson and alldata.csv

When the routes are generated, you can close the services by executing the two following instructions.

CONTAINER_ID_BACKEND=$(sudo docker ps | egrep -i osrm-backend | cut -d' ' -f1)
sudo docker stop ${CONTAINER_ID_BACKEND}

#Analysis of the data

#Routes examples reproduction
