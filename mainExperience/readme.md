In this folder, you will find the Python script to generate the routes, the routes used for the section 4 in the geojson format and a shapefile version obtained in QGIS 
(it goes a lot faster)

You will also find a R markdown file where the data is analysed and the figure 2, 3 and 4 are obtainable from this script.

The figures 5, 6 and 7 are screenshots taken from QGIS. Here are the guidelines to obtain them.

When QGIS is opened, load the layer alldataZones.shp (use the shapefile to win some time). Then, go in the layer's properties, in the "Source" tab, click on "Query Builder" to filter the layer with the following expression:
"city"='Blois' and "idTrace" IN (523,162) and "year" IN (2014, 2019, 2020, 2021, 2022)
In the layer's properties, in the "Symbology" tab, change "Single symbol" to "Categorized" and use the "year" attribute. The following colors refers for the years:
- 2014, black
- 2019, purple
- 2020, dark blue
- 2021, neon green
- 2022, brown

You can add the start and end point by using the tool "Extract Specific Vertices". As parameters, choose alldata.shp as input layer, for "Vertex indices" write 0,-1 and you can launch the tool. A layer named "Vertices" should appear in the "Layers" menu. On the properties of that new layer, in the "Symbology" tab, change "Single symbol" to "Categorized" and use the "vertex_pos" attribute with the 0 in red and the -1 in green.
The traces for the other years are hidden behind the others so you can let them as you want.

On the map, figure 5 is on the top right, figure 6 is on the bottom and figure 7 is on the top left.
