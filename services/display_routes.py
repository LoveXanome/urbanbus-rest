# -*- coding: utf-8 -*-

from database.database_access import get_dao, get_urban, get_lat_lng
from gtfslib.model import Route

def get_routes(agency_id, limit=None):
	dao = get_dao(agency_id)
	data = dict()
	parsedRoutes = list()
	data['agency'] = "TAN"
	data['location'] = get_lat_lng(agency_id)
	countRoutes = 0

	urban_routes = get_urban(agency_id)

	for route in dao.routes(fltr=Route.route_type == Route.TYPE_BUS):
		countRoutes += 1
		if limit and countRoutes > limit:
			break
		parsedRoute = dict()
		parsedRoute["id"] = route.route_id
		parsedRoute["name"] = route.route_long_name
		parsedRoute["category"] = urban_routes[route.route_id]
		parsedRoutes.append(parsedRoute)

	data['routes'] = parsedRoutes
	return data

