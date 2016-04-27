# -*- coding: utf-8 -*-

import json
from gtfslib.dao import Dao
from gtfslib.model import Agency

def get_agencies():
	dao = Dao("services/db.sqlite")
	lines = []

	for agency in dao.agencies():
		line = dict()
		line["name"] = agency.agency_name

		line["id"] = agency.agency_id

		lines.append(line)
	return json.dumps(lines, sort_keys=True, indent=4, separators=(',', ': '))
