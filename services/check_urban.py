# -*- coding: utf-8 -*-

import json
from gtfslib.dao import Dao
from gtfslib.model import Route
from gtfsplugins import decret_2015_1610

def get_urban_status():
	dao = get_dao()
	lines = []

	for route in dao.routes(fltr=Route.route_type == Route.TYPE_BUS):
		# routes = dao.routes(fltr=Route.route_type == Route.TYPE_BUS)
		# route = routes[0]
		line = dict()
		line["name"] = route.route_long_name

		trips = list(route.trips)
		category = decret_2015_1610.decret_2015_1610(trips)
		line["category"] = str(category)

		lines.append(line)
		print line
	return lines
