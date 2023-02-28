# AGILE2023-reproduction
This repository is here to reproduct the article "Analysis of cycling network evolution in OpenStreetMap through a data quality prism" submitted at AGILE 2023 conference

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
- geojson (pip install geojson)
- csv (pip install csv)

##R 4.1
This link explains how to install R for our operating system (https://linuxize.com/post/how-to-install-r-on-ubuntu-20-04/)

##QGIS 3.*
Follow this link to install QGIS (https://www.qgis.org/en/site/forusers/alldownloads.html#linux)

#Data download

The data used during the experiment is provided by Geofabrik (https://osm-internal.download.geofabrik.de/europe/france/centre.html?oauth_token_secret_encr=pIX6N_buN6DEYifrzq1hT1Y4r8Do_dOcalIU9idjIbX500LRwk6ozHhXK601AAMGcw-vXd3jEGWv8cyBk45hPibsJrzu7YPhB5Y508SzEEI%3D&oauth_token=zUhruGhV49VAMsDyQa75pQSgzhXwO4f9HJegn8np).
The data used was every snapshot at January the 1st from 2014 to 2022 included.

#Network generation

Here is an example for the 2014 snapshot in Centre Val-de-Loire region. Repeat it for every network you want.
The following instructions create a cycling network based on our data extracted from Geofabrik.

When that step is done, open a terminal and write the following instructions.

cd working/directory

docker run -t -v "${PWD}:/path/to/store/data/2014" osrm/osrm-backend osrm-extract -p /opt/bicycle.lua /path/to/data/centre2014.osm.pbf

sudo docker run -t -v "${PWD}:/path/to/store/data/2014" osrm/osrm-backend osrm-partition /path/to/data/centre2014.osrm

sudo docker run -t -v "${PWD}:/path/to/store/data/2014" osrm/osrm-backend osrm-customize /path/to/data/centre2014.osrm

#Route generation

You first need to turn the services on. The parameter 5014 should be changed for each network if you want to run multiple networks at the same time. For this experiment, the 5014 number corresponds to 3000 + year of the OSM snapshot. Run in a terminal that instruction to open the access to one network. Repeat it for every other network you want. It is possible to launch multiple networks on the same terminal.

sudo docker run -d -p 5014:5000 -v "/path/to/store/data:/data" osrm/osrm-backend osrm-routed --algorithm mld /path/to/data/centre2014.osrm

You can now launch the Python script to generate the routes and modify Line 163 and 166 with a path where the GEOJSON and the CSV file should be saved. If you have chosen another area, you should change the bounding box in the script. The results are two files named alldataZones.geojson and alldata.csv

When the routes are generated, you can close the services by executing the two following instructions.

CONTAINER_ID_BACKEND=$(sudo docker ps | egrep -i osrm-backend | cut -d' ' -f1)
sudo docker stop ${CONTAINER_ID_BACKEND}

#Analysis of the data

The data used for the analysis is available here (https://utbox.univ-tours.fr/s/xKFo5BJgAHtnAmK). If you use data you have generated yourself, the numbers can slightly change from the ones in the paper.

Table 2 and 3 have been assembled with data computed in the Rmarkdown file available in this deposit.
Line 17 should be modified with the path to the CSV file generated in the route generation step


#Routes examples reproduction

The Figure 5,6 and 7 are screenshots taken from QGIS with a legend added after the screenshot. Here are the guidelines to obtain them.

When QGIS is opened, load the layer alldataZones.shp (use the shapefile to win some time but you can also use the geojson generated from the Python script). Then, go in the layer's properties, in the "Source" tab, click on "Query Builder" to filter the layer with the following expression: "city"='Blois' AND (("idTrace" = 523 AND year IN (2014, 2019, 2020, 2021, 2022)) OR ("idTrace"=162 AND "year" in (2020, 2021))) It should return 7 objects. In the layer's properties, in the "Symbology" tab, change "Single symbol" to "Categorized" and use the "year" attribute. The following colors refers for the years:

- 2014, black
- 2019, purple
- 2020, dark blue
- 2021, neon green
- 2022, brown

You can add the starting and ending point by using the tool "Extract Specific Vertices" from the toolbox. As parameters, choose the routes file as input layer, for "Vertex indices" write 0,-1 (0 for starting and -1 for ending) and you can launch the tool. A layer named "Vertices" should appear in the "Layers" menu. On the properties of that new layer, in the "Symbology" tab, change "Single symbol" to "Categorized" and use the "vertex_pos" attribute with the 0 in red and the -1 in green. The traces for the other years are hidden behind the others so you can raise the hidden layers' width.

On the map, Figure 5 and 6 are on the right route. Figure 5 is around the starting point and Figure 6 around the ending point. Figure 7 is on the left route.
