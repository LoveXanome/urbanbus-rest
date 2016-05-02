# -*- coding: utf-8 -*-

from database.database_access import get_average_speed

def get_avg_speed(agency_id, route_id, stop_id):
	vitesse = get_average_speed(agency_id, stop_id, route_id)
	return vitesse	
