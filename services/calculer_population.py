# -*- coding: utf-8 -*-

from database.database_access import get_dao, get_all_agencies, fill_population_table, get_urban
from gtfslib.model import Route, Agency
from gtfslib.dao import Dao
from services.get_route import get_population_stops

def calculer_pop():
	agencies = get_all_agencies()
	
	for agency in agencies:
		dao = get_dao(agency.id)
		parsedRoutes = list()
		countRoutes = 0

		urban_routes = get_urban(agency.id)

		for route in dao.routes(fltr=Route.route_type == Route.TYPE_BUS):
			listeroutes = get_population_stops(agency.id,route.route_id)
			print('Insertion des stops de ' + route.route_id)
			for stop in listeroutes :	
				stop_id = stop['id']
				population = stop['population']
				fill_population_table(agency.id, stop_id, population)
	return True