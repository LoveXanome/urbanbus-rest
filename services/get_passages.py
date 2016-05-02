# -*- coding: utf-8 -*-

from database.database_access import get_passages

def get_nb_passages(agency_id, route_id, stop_id):
	passages = get_passages(agency_id, stop_id, route_id)
	return passages	
