# -*- coding: utf-8 -*-

from database.database_access import get_dao
from gtfslib.model import Route, StopTime, Shape
from gtfsplugins import decret_2015_1610
from database.database_access import get_dao
from services.check_urban import check_urban_category

def get_route(agency_id, routeId):
	dao = get_dao(agency_id)
	parsedRoute = dict()
	listPoints = list()

	route = dao.routes(fltr=Route.route_id == routeId)
	print(route)
	parsedRoute["id"] = route[0].route_id
	parsedRoute["name"] = route[0].route_long_name
	parsedRoute["category"] = check_urban_category(route[0].trips)
	# All trips have same trip_id so we may use only the first : route.trips[0]
	_get_route_shapepoints(dao, route[0].trips[0].shape_id, listPoints)
	_get_route_stops(dao, route[0].trips[0].trip_id, listPoints)
	parsedRoute['points'] = listPoints
			
	return parsedRoute

'''	Private methods '''

def _get_route_shapepoints(dao, shapeId, listPoints):
	countPoints = 0

	shape = dao.shape(shapeId)
	
	if shape is not None:
		for point in shape.points:
			countPoints += 1
			parsedPoint = dict()
			parsedPoint['id'] = str(point.feed_id)+str(point.shape_id)+str(point.shape_pt_sequence)
			parsedPoint['name'] = "no_name"
			parsedPoint['is_stop'] = False
			parsedPoint['lat'] = point.shape_pt_lat
			parsedPoint['lng'] = point.shape_pt_lon
			listPoints.append(parsedPoint)

	print('Nb shape points = '+str(countPoints))
	return

def _get_route_stops(dao, tripId, listPoints):
	countStops = 0

	stoptimes = dao.stoptimes(fltr=StopTime.trip_id == tripId)

	for stoptime in stoptimes:
		stop = dao.stop(stoptime.stop_id)

		if stop is not None:
			countStops += 1
			parsedStop = dict()
			parsedStop['id'] = stop.stop_id
			parsedStop['name'] = stop.stop_name
			parsedStop['is_stop'] = True
			parsedStop['lat'] = stop.stop_lat
			parsedStop['lng'] = stop.stop_lon
			if not _check_already_in(listPoints, parsedStop):
				listPoints.append(parsedStop)

	print('Nb stop points = '+str(countStops))
	return 


def _same_position(pointA, pointB):
	return pointA.get('lat') == pointB.get('lat') and pointA.get('lng') == pointB.get('lng')

def _set_is_stop(pointToModifiy, stop):
	pointToModifiy['is_stop'] = True
	pointToModifiy['name'] = "tralala"
	pointToModifiy['id'] = stop['id']

def _check_already_in(points, aPoint):
	for point in points:
		if _same_position(point, aPoint):
			_set_is_stop(point, aPoint)
			return True
	return False