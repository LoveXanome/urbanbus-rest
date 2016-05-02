# -*- coding: utf-8 -*-

from database.database_access import get_dao, get_urban, get_lat_lng
from gtfslib.model import Route

def get_routes(agency_id, limit=None):
	dao = get_dao(agency_id)
	parsedRoutes = list()
	countRoutes = 0

	urban_routes = get_urban(agency_id)

	for route in dao.routes(fltr=Route.route_type == Route.TYPE_BUS):
		countRoutes += 1
		if limit and countRoutes > limit:
			break
		parsedRoute = dict()
		parsedRoute["id"] = route.route_id
		parsedRoute["short_name"] = route.route_short_name
		parsedRoute["name"] = route.route_long_name
		parsedRoute["category"] = urban_routes[route.route_id]["category"]
		parsedRoute["interdistance"] = urban_routes[route.route_id]["interdistance"]
		parsedRoute["ratio"] = urban_routes[route.route_id]["ratio"] if(urban_routes[route.route_id]["ratio"] != float("inf")) else None
		parsedRoutes.append(parsedRoute)

	return sorted(parsedRoutes, key=lambda k: k['name'])
