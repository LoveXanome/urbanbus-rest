# -*- coding: utf-8 -*-

from database.database_access import get_agency_by_id

def get_agency(agency_id):
	parsedAgency = dict()
	agency = get_agency_by_id(agency_id)
	parsedAgency['id'] = agency.agency_id
	parsedAgency['name'] = agency.agency_name
	parsedAgency['location'] = { 'lat': agency.latitude, 'lng': agency.longitude }
		
	return parsedAgency	
