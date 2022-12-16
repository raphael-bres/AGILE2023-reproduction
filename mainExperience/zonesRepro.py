import numpy as np
import requests
from geojson import Feature, FeatureCollection, dump
import csv


def nearest_road_point(lon, lat, year):
	loc = "{},{}".format(lon, lat)
	y = year + 3000
	url = "http://127.0.0.1:"  # define your OSRM server address here
	url2 = "/nearest/v1/biking/"
	r = requests.get(url + str(y) + url2 + loc)
	if r.status_code != 200:
		return {}
	res = r.json()
	nearest_point = res['waypoints'][0]['location']
	dist = res['waypoints'][0]['distance']
	return nearest_point, dist


def get_route(start_lon, start_lat, end_lon, end_lat, year):
	loc = "{},{};{},{}".format(start_lon, start_lat, end_lon, end_lat)
	y = year + 3000
	url = "http://127.0.0.1:" + str(y) + "/route/v1/biking/"  # define your OSRM server address here
	url2 = "?overview=full&geometries=geojson&annotations=true"
	r = requests.get(url + loc + url2)
	if r.status_code != 200:
		return {}
	res = r.json()
	geometry = res['routes'][0]['geometry']
	coords = res['routes'][0]['geometry']['coordinates']
	distance = res['routes'][0]['distance']
	duration = res['routes'][0]['duration']
	start_point = [res['waypoints'][0]['location'][1], res['waypoints'][0]['location'][0]]
	end_point = [res['waypoints'][1]['location'][1], res['waypoints'][1]['location'][0]]
	out = {
		'geometry': geometry,
		'coords': coords,
		'distance': distance,
		'duration': duration,
		'start_point': start_point,
		'end_point': end_point
	}
	return out


def check_point(point):
	# Check if a point is always matched to the same point in all my road networks
	lon = point[0]
	lat = point[1]
	coords = []
	# Fill coords with the matched points of the different years.
	# for ends in 2019 because lon and lat are the 2020 point
	for i in range(2014, 2022):
		point, dist = nearest_road_point(lon, lat, i)
		coords.append(point)
	# If there are some different points in coords we return false
	equal = True
	for c in coords:
		if c[0] != lon or c[1] != lat:
			equal = False
			break
	return equal


def find_start(distance, bb):
	d = distance + 1
	b = False
	# Repeat while distance between most recent network and point is superior to 50m
	while d > distance or not b:
		# Find a starting point
		lon_depart = np.random.uniform(bb[0][0], bb[1][0])
		lat_depart = np.random.uniform(bb[1][1], bb[0][1])
		start_point, d = nearest_road_point(lon_depart, lat_depart, 2022)
		b = check_point(start_point)
	return [lon_depart, lat_depart],d


def find_end(start_point, distance):
	# Get the coordinates from start point
	start_lon = start_point[0]
	start_lat = start_point[1]
	# We need the random point and the matched point to have a distance of less than d meters
	d = distance + 1
	b = False
	while d > distance or not b:
		lon_signe = np.random.uniform(0, 2)
		lat_signe = np.random.uniform(0, 2)
		# A choice is made to stay on the same side of the starting point
		if lon_signe >= 1:
			lon_arrive = np.random.uniform(start_lon + 0.00225, start_lon + 0.04452)
		else:
			lon_arrive = np.random.uniform(start_lon - 0.04452, start_lon - 0.00225)
		if lat_signe >= 1:
			lat_arrive = np.random.uniform(start_lat + 0.00225, start_lat + 0.04452)
		else:
			lat_arrive = np.random.uniform(start_lat - 0.04452, start_lat - 0.00225)
		end_point, d = nearest_road_point(lon_arrive, lat_arrive, 2022)
		b = check_point(end_point)
	return end_point,d

#Begin by defining your working directory
# loop over the number of routes we want
#bboxes takes the coordinates of the top left point then the bottom right point
bboxes = [[[0.6445009, 47.421435], [0.713116, 47.348574]], [[1.876152, 47.920526], [1.925675, 47.879144]], [[1.290498, 47.613294], [1.367060, 47.573531]], [[2.383943, 47.092806], [2.430874, 47.055626]], [[1.907606, 47.741261], [2.305352, 47.419778]], [[1.526775, 48.370851], [1.834774, 48.055433]]]
cities = ["Tours", "Orleans", "Blois", "Bourges", "Sologne", "Beauce"]
#Distance to the network
d = 100
#Variable who will contain the data for the geojson
z = []
#Header of the CSV file
dataCSV=[["city","idTrace","year","duration","distance","diffDur","pctDiffDur","diffDist","pctDiffDist"]]
for b in range(len(cities)):
	for k in range(1, 51):
		#console print to know where we are during the execution
		print(cities[b]+" "+str(k))
		# find start point then find end point
		start_point, dist2nets = find_start(d, bboxes[b])
		end_point, dist2nete = find_end(start_point, d)
		#dInf returns false if one route has a length superior than 5000
		#dSup returns false if one route has a length inferior than 300
		#du returns false if one route has a duration of 0
		dInf = True
		dSup = True
		du = True
		dis = True
		#We dp not want any of the above criterias to generate the routes
		while dInf or dSup or du or dis:
			start_point, dist = find_start(d, bboxes[b])
			end_point, di = find_end(start_point, d)
			req = get_route(start_point[0], start_point[1], end_point[0], end_point[1], 2022)
			req2 = get_route(start_point[0], start_point[1], end_point[0], end_point[1], 2021)
			req3 = get_route(start_point[0], start_point[1], end_point[0], end_point[1], 2020)
			req4 = get_route(start_point[0], start_point[1], end_point[0], end_point[1], 2019)
			req5 = get_route(start_point[0], start_point[1], end_point[0], end_point[1], 2018)
			req6 = get_route(start_point[0], start_point[1], end_point[0], end_point[1], 2017)
			req7 = get_route(start_point[0], start_point[1], end_point[0], end_point[1], 2016)
			req8 = get_route(start_point[0], start_point[1], end_point[0], end_point[1], 2015)
			req9 = get_route(start_point[0], start_point[1], end_point[0], end_point[1], 2014)
			dInf = req["distance"] > 5000 and req2["distance"] > 5000 and req3["distance"] > 5000 and req4["distance"] > 5000 and req5["distance"] > 5000 and req6["distance"] > 5000 and req7["distance"] > 5000 and req8["distance"] > 5000 and req9["distance"] > 5000
			dSup = req2["distance"] < 500 and req["distance"] < 300 and req3["distance"] < 300 and req4["distance"] < 300 and req5["distance"] < 300 and req6["distance"] < 300 and req7["distance"] < 300 and req8["distance"] < 300 and req9["distance"] < 300
			du = req["duration"] == 0 and req2["duration"] == 0 and req3["duration"] == 0 and req4["duration"] == 0 and req5["duration"] == 0 and req6["duration"] == 0 and req7["duration"] == 0 and req8["duration"] == 0 and req9["duration"] == 0
			dis = req["distance"] == 0 and req2["distance"] == 0 and req3["distance"] == 0 and req4["distance"] == 0 and req5["distance"] == 0 and req6["distance"] == 0 and req7["distance"] == 0 and req8["distance"] == 0 and req9["distance"] == 0
		#When we are here, the starting and ending points are defined for one route. Starting generation of the route for each year
		for year in range(2014, 2023):
			# Find the route for each year
			req = get_route(start_point[0], start_point[1], end_point[0], end_point[1], year)
			route_json = req['geometry']
			route_time = req['duration']
			route_dist = req['distance']
			if year == 2014: #if year is the first year of the analysis we can't have any data
				diffDur = 0
				diffDist = 0
			else:
				diffDur = route_time - lastYearDur
				diffDist = route_dist - lastYearDist
			lastYearDur = route_time
			lastYearDist = route_dist
			dataCSV.append([cities[b], k, year, route_time, route_dist, diffDur, diffDur/route_time*100, diffDist, diffDist/route_dist*100])
			z.append(Feature(geometry=route_json, properties={"city": cities[b], "idTrace": k, "year": year, "duration": route_time, "distance": route_dist, "diffDur": diffDur, "pctDiffDur": diffDur/route_time*100, "diffDist": diffDist, "pctDiffDist": diffDist/route_dist*100}))
		# Put some info into a geojson file
		feat_col = FeatureCollection(z)
with open("path/you/want/dataZones.csv", "w",newline='') as f:
	writer = csv.writer(f)
	writer.writerows(dataCSV)
with open("path/you/want/alldataZones.geojson", 'w') as file:
	dump(feat_col, file)
print("all data done")

"""Execution times for 1000 routes per area with 9 years:
	Tours 9min23
	Orleans 8min27
	Blois 7min58
	Bourges 6min17
	Sologne 18min25
	Beauce 8min56
	geojson dump 55s
	TOTAL 1h00min21s"""

