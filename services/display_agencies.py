# -*- coding: utf-8 -*-

from gtfslib.dao import Dao
from gtfslib.model import Agency
from database.database_access import get_dao

def get_agencies():
	dao = get_dao()
	lines = []

	for agency in dao.agencies():
		line = dict()
		line["name"] = agency.agency_name

		line["id"] = agency.agency_id

		lines.append(line)
	return lines
