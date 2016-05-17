# -*- coding: utf-8 -*-

import json
from gtfslib.dao import Dao
from gtfslib.model import Route
from gtfsplugins import decret_2015_1610
from database.database_access import get_dao

def get_urban_status(agency_id):
    dao = get_dao(agency_id)
    lines = []

    for route in dao.routes(fltr=Route.route_type == Route.TYPE_BUS):
        line = dict()
        line["name"] = route.route_long_name
        line["category"] = check_urban_category(route.trips)
        lines.append(line)
    return lines

def check_urban_category(trips):
    return decret_2015_1610.decret_2015_1610(trips)