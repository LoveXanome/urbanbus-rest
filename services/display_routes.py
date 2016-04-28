# -*- coding: utf-8 -*-

import json
from database.database_access import get_dao
from gtfslib.model import Route
from gtfsplugins import decret_2015_1610

def get_routes(agency_id):
	dao = get_dao(agency_id)
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
