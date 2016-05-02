# -*- coding: utf-8 -*-

from database import database_access as db
from services.display_population_insee import get_population_insee

def calculate_population(dbname, dataset_id):
    full_dbname = db._get_complete_database_name(dbname)
    engine = db._create_urban_table(full_dbname)
    with engine.connect() as con:
        sql_result = con.execute("SELECT * FROM stops")
        # TODO count for progress
        for stop in sql_result:
            print(stop, flush=True)
            pop = get_population_insee(stop.stop_lon, stop.stop_lat, 200)
            print(pop, flush=True)
            db.fill_population_table(dataset_id, stop.stop_id, pop)

    
    