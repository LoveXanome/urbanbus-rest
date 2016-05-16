# -*- coding: utf-8 -*-

from database import database_access as db
from services.insee import get_population_insee

def calculate_population(dbname, dataset_id):
    full_dbname = db._get_complete_database_name(dbname)
    engine = db._create_urban_table(full_dbname)
    with engine.connect() as con:
        sql_result = con.execute("SELECT * FROM stops")
        for stop in sql_result:
            pop = get_population_insee(stop.stop_lat, stop.stop_lon, 200)
            db.fill_population_table(dataset_id, stop.stop_id, pop)
            db.inc_nb_population(dataset_id)

def nb_stops(dbname):
    full_dbname = db._get_complete_database_name(dbname)
    engine = db._create_urban_table(full_dbname)
    with engine.connect() as con:
        sql_result = con.execute("SELECT COUNT(*) FROM stops")
        for c in sql_result:
            return c[0]