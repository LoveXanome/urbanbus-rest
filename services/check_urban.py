# -*- coding: utf-8 -*-

import json
from gtfslib.dao import Dao
from gtfslib.model import Route
from gtfsplugins import decret_2015_1610

def get_urban_status():
	dao = Dao("database/db.sqlite")
	lines = []

	for route in dao.routes(fltr=Route.route_type == Route.TYPE_BUS):
		# routes = dao.routes(fltr=Route.route_type == Route.TYPE_BUS)
		# route = routes[0]
		line = dict()
		line["name"] = route.route_long_name

		trips = list(route.trips)
		urbain = decret_2015_1610.decret_2015_1610(trips)
		line["urban"] = str(urbain)

		lines.append(line)
	return json.dumps(lines, sort_keys=True, indent=4, separators=(',', ': '))
