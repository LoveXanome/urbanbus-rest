# -*- coding: utf-8 -*-

from gtfslib.model import Route, StopTime, Shape
from database.database_access import get_dao, get_urban_by_id, get_stop_routes

def get_stop(agency_id, stop_id):
	dao = get_dao(agency_id)
	parsedStop = dict()
	listRoute = list()

	stop = dao.stop(stop_id)

	if stop:
		parsedStop['id'] = stop.stop_id or ''
		parsedStop['name'] = stop.stop_name or ''
		parsedStop['is_stop'] = True 
		parsedStop['location'] = {'lat': stop.stop_lat or '', 'lng': stop.stop_lon or ''}


	routes = get_stop_routes(agency_id, stop_id)
	return parsedStop


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
			parsedStop['location'] = {'lat': stop.stop_lat, 'lng': stop.stop_lon}
			listPoints.append(parsedStop)

	print('Nb stop points = '+str(countStops))
	return 
