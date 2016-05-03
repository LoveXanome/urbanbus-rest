# -*- coding: utf-8 -*-

from gtfslib.model import Route, StopTime, Shape
from database.database_access import get_dao, get_urban_by_id, get_stop_routes, get_population
from .get_avg_speed import get_avg_speed
from .get_passages import get_passages

def get_stop(agency_id, stop_id):
	dao = get_dao(agency_id)
	parsedStop = dict()
	
	stop = dao.stop(stop_id)

	if stop:
		parsedStop['id'] = stop.stop_id or ''
		parsedStop['name'] = stop.stop_name or ''
		parsedStop['is_stop'] = True 
		parsedStop['location'] = {'lat': stop.stop_lat or '', 'lng': stop.stop_lon or ''}
		parsedStop['population_200m'] = get_population(agency_id, stop_id) or None
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
		parsedRoute['average_speed'] = get_avg_speed(agency_id, route.route_id, stop_id)
		parsedRoute['passages'] = get_passages(agency_id, stop_id, route.route_id)
		listRoutes.append(parsedRoute)

	return listRoutes
