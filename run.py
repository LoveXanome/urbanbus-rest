# -*- coding: utf-8 -*-

from gtfslib.dao import Dao

dao = Dao("services/db.sqlite")
dao.load_gtfs("nantes.zip")
print("Chargement OKAY")
