# -*- coding: utf-8 -*-

from database import database_access
from gtfslib.model import Agency
from gtfslib.dao import Dao

def get_agencies():
	agencies = database_access.get_all_agencies()
	agencies_list = list()
	
	for agency in agencies:
		agencies_list.append({'name': agency.agency_name, 'id': agency.id})
		
	return agencies_list	
