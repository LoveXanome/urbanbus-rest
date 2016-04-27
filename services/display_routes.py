# -*- coding: utf-8 -*-

import json
from database.database_access import get_dao
from gtfslib.model import Route
from gtfsplugins import decret_2015_1610

def get_routes():
	dao = get_dao()
	parsedRoutes = []

	for route in dao.routes(fltr=Route.route_type == Route.TYPE_BUS):
		parsedRoute = dict()
		parsedRoute["name"] = route.route_long_name

		parsedRoutes.append(parsedRoute)
	return parsedRoutes
