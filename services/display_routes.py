# -*- coding: utf-8 -*-

from database.database_access import get_dao
from gtfslib.model import Route
from services.check_urban import check_urban_category

def get_routes(agency_id):
	dao = get_dao(agency_id)
	data = dict()
	parsedRoutes = list()
	data['agency'] = "TAN"
	data['location'] = {'lat': 48.6843900, 'lng': 6.1849600}

	for route in dao.routes(fltr=Route.route_type == Route.TYPE_BUS):
		print(route)
		parsedRoute = dict()
		parsedRoute["id"] = route.route_id
		parsedRoute["name"] = route.route_long_name
		parsedRoute["category"] = check_urban_category(route.trips)
		parsedRoutes.append(parsedRoute)

	data['routes'] = parsedRoutes
	return data

