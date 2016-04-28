# -*- coding: utf-8 -*-

from database.database_access import get_dao
from gtfslib.model import Route, StopTime, Shape
from gtfsplugins import decret_2015_1610
from database.database_access import get_dao
from services.check_urban import check_urban_category

def get_routes_details(limit):
	dao = get_dao()
	parsedRoutes = []
	count = 0
	for route in dao.routes(fltr=Route.route_type == Route.TYPE_BUS):
		if count < limit:
			count+=1
			parsedRoute = dict()
			
			parsedRoute["name"] = route.route_long_name
			parsedRoute["category"] = check_urban_category(route.trips)
			# All trips have same trip_id so we may use only the first : route.trips[0]
			parsedRoute['points'] = get_route_shapepoints(dao, route.trips[0].shape_id)
			parsedRoute['stops'] = get_route_stops(dao, route.trips[0].trip_id)

			parsedRoutes.append(parsedRoute)
			
			print('Nb of equal points = ', count_equal_points(parsedRoute))
	return parsedRoutes

def get_stoptime():
	pass

def equal_point(pointA, pointB):
	return pointA.get('lat') == pointB.get('lat') and pointA.get('lng') == pointB.get('lng')

def count_equal_points(route):
	countEqual = 0
	for point in route.get('points'):
		for stop in route.get('stops'):
			if equal_point(point, stop):
				countEqual += 1
				break
	return countEqual

def get_route_stops(dao, tripId):
	parsedStops = list()
	countStops = 0

	stoptimes = dao.stoptimes(fltr=StopTime.trip_id == tripId)

	for stoptime in stoptimes:
		stop = dao.stop(stoptime.stop_id)

		if stop is not None:
			countStops += 1
			parsedStop = dict()
			parsedStop['id'] = stop.stop_id
			parsedStop['name'] = stop.stop_name
			parsedStop['lat'] = stop.stop_lat
			parsedStop['lng'] = stop.stop_lon
			parsedStops.append(parsedStop)

	print('Nb stop points = ', countStops)
	return parsedStops

def get_route_shapepoints(dao, shapeId):
	parsedPoints = list()
	countPoints = 0

	shape = dao.shape(shapeId)
	
	if shape is not None:
		for point in shape.points:
			print(point)
			countPoints += 1
			parsedPoint = dict()
			parsedPoint['id'] = str(point.feed_id)+str(point.shape_id)+str(point.shape_pt_sequence)
			parsedPoint['lat'] = point.shape_pt_lat
			parsedPoint['lng'] = point.shape_pt_lon
			parsedPoints.append(parsedPoint)

	print('Nb shape points = ', countPoints)
	return parsedPoints
