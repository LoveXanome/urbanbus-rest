# -*- coding: utf-8 -*-

from database.database_access import get_all_agencies
from gtfslib.model import Agency
from gtfslib.dao import Dao

def get_agencies():
	agencies = get_all_agencies()
	agencies_list = list()
	
	for agency in agencies:
		agencies_list.append({'name': agency.agency_name, 'id': agency.id})
		
	return agencies_list	
