# -*- coding: utf-8 -*-

from gtfslib.model import Route, StopTime, Shape
from database.database_access import get_dao, get_urban_by_id, get_stop_routes

def get_stop(agency_id, stop_id):
	dao = get_dao(agency_id)
	parsedStop = dict()
	
	stop = dao.stop(stop_id)

	if stop:
		parsedStop['id'] = stop.stop_id or ''
		parsedStop['name'] = stop.stop_name or ''
		parsedStop['is_stop'] = True 
		parsedStop['location'] = {'lat': stop.stop_lat or '', 'lng': stop.stop_lon or ''}
		parsedStop['routes'] = _get_routes(agency_id, stop_id)
	return parsedStop


'''	Private methods '''

def _get_routes(agency_id, stop_id):
	listRoutes = list()

	routes = get_stop_routes(agency_id, stop_id)
	for route in routes:
		parsedRoute = dict()
		parsedRoute['id'] = route.route_id
		parsedRoute['name'] = route.route_long_name
		parsedRoute['short_name'] = route.route_short_name
		listRoutes.append(parsedRoute)

	return listRoutes
