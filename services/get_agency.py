# -*- coding: utf-8 -*-

from database.database_access import get_agency_by_id

def get_agency(agency_id):
	agency = get_agency_by_id(agency_id)
	print(str(agency))
	print('yo')
		
	return agency	
