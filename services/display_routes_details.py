# -*- coding: utf-8 -*-

from database.database_access import get_dao
from gtfslib.model import Route, StopTime, Shape
from gtfsplugins import decret_2015_1610
from database.database_access import get_dao

def get_routes_details(limit):
	dao = get_dao()
	parsedRoutes = []
	count = 0
	for route in dao.routes(fltr=Route.route_type == Route.TYPE_BUS):
		if count < limit:
			parsedRoute = dict()
			parsedStops = list()
			parsedPoints = list()
			parsedRoute["name"] = route.route_long_name
			count+=1
			
			# All trips have same trip_id so we may use only the first
			shape = dao.shape(route.trips[0].shape_id)
			
			countPoints = 0
			if shape is not None:
				for point in shape.points:
					countPoints += 1
					parsedPoint = dict()
					parsedPoint['lat'] = point.shape_pt_lat
					parsedPoint['lng'] = point.shape_pt_lon
					parsedPoints.append(parsedPoint)
				parsedRoute['points'] = parsedPoints

			# All trips have same trip_id so we may use only the first
			stoptimes = dao.stoptimes(fltr=StopTime.trip_id == route.trips[0].trip_id)
			print "nb of trips: "+str(len(route.trips))
			print "ID trip used: "+str(route.trips[0].trip_id)
			print "trip headsign used: "+route.trips[0].trip_headsign.encode('ASCII', 'ignore')
			#print stoptimes

			countStops = 0
			for stoptime in stoptimes:
				stop = dao.stop(stoptime.stop_id)
				parsedStop = dict()
				if stop is not None:
					countStops += 1
					parsedStop['name'] = stop.stop_name
					parsedStop['lat'] = stop.stop_lat
					parsedStop['lng'] = stop.stop_lon
				parsedStops.append(parsedStop)

			parsedRoute['stops'] = parsedStops
			parsedRoutes.append(parsedRoute)
			print('Nb shapepoints = ', countPoints)
			print('Nb stoppoints = ', countStops)
			print('Nb of equal points = ', count_equal_points(parsedPoints, parsedStops))
	return parsedRoutes

def get_stoptime():
	pass

def equal_point(pointA, pointB):
	return pointA.get('lat') == pointB.get('lat') and pointA.get('lng') == pointB.get('lng')

def count_equal_points(points, stops):
	countEqual = 0
	for point in points:
		for stop in stops:
			if equal_point(point, stop):
				countEqual += 1
				break
	return countEqual