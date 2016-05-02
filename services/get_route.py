# -*- coding: utf-8 -*-

from gtfslib.model import Route, StopTime, Shape
from database.database_access import get_dao, get_urban_by_id
from services.display_population_insee import get_population_insee
populationTotale = 0

def get_route(agency_id, route_id):
	dao = get_dao(agency_id)
	parsedRoute = dict()
	listPoints = list()
	listStops = list()

	route = dao.route(route_id)
	parsedRoute["id"] = route.route_id
	parsedRoute["short_name"] = route.route_short_name
	parsedRoute["name"] = route.route_long_name
	urban = get_urban_by_id(agency_id, route_id)
	parsedRoute["category"] = urban["category"]
	parsedRoute["interdistance"] = urban["interdistance"]
	parsedRoute["ratio"] = urban["ratio"] if(urban["ratio"] != float("inf")) else None

	# All trips have same trip_id so we may use only the first : route.trips[0]
	if len(route.trips) is not 0:
		_get_route_shapepoints(dao, route.trips[0].shape_id, listPoints)
		parsedRoute['points'] = listPoints
		_get_route_stops(dao, route.trips[0].trip_id, listStops)
		parsedRoute['stops'] = listStops
			
	return parsedRoute
	
def get_population(agency_id, route_id):
	dao = get_dao(agency_id)
	parsedRoute = dict()
	listPoints = list()

	route = dao.route(route_id)
	parsedRoute["id"] = route.route_id
	parsedRoute["short_name"] = route.route_short_name
	parsedRoute["name"] = route.route_long_name
	parsedRoute["category"] = get_urban_by_id(agency_id, route_id)

	# All trips have same trip_id so we may use only the first : route.trips[0]
	if len(route.trips) is not 0:
		_get_route_shapepoints(dao, route.trips[0].shape_id, listPoints)
		_get_route_stops(dao, route.trips[0].trip_id, listPoints, True)
	parsedRoute['points'] = listPoints
	parsedRoute['population_totale'] = populationTotale
			
	return parsedRoute
	
def get_population_stops(agency_id,route_id):
	dao = get_dao(agency_id)
	parsedRoute = dict()
	listPoints = list()

	route = dao.route(route_id)

	# All trips have same trip_id so we may use only the first : route.trips[0]
	if len(route.trips) is not 0:
		_get_route_stops(dao, route.trips[0].trip_id, listPoints, True)
			
	return listPoints

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
			parsedPoint['location'] = {'lat': point.shape_pt_lat, 'lng': point.shape_pt_lon}
			listPoints.append(parsedPoint)

	print('Nb shape points = '+str(countPoints))
	return

def _get_route_stops(dao, tripId, listPoints, avecPopulation = False):
	global populationTotale
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
			parsedStop['location'] = {'lat': stop.stop_lat, 'lng': stop.stop_lon}
			if avecPopulation :
				parsedStop['population'] = get_population_insee(stop.stop_lon,stop.stop_lat,200)
				populationTotale = populationTotale + parsedStop['population']
			if not _check_already_in(listPoints, parsedStop):
				listPoints.append(parsedStop)

	print('Nb stop points = '+str(countStops))
	return


def _same_position(pointA, pointB):
	return pointA['location'].get('lat') == pointB['location'].get('lat') and pointA['location'].get('lng') == pointB['location'].get('lng')

def _set_is_stop(pointToModifiy, stop):
	pointToModifiy['is_stop'] = True
	pointToModifiy['name'] = stop['name']
	pointToModifiy['id'] = stop['id']

def _check_already_in(points, aPoint):
	for point in points:
		if _same_position(point, aPoint):
			_set_is_stop(point, aPoint)
			return True
	return False