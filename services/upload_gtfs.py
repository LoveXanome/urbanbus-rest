# -*- coding: utf-8 -*-

from datetime import datetime
import os
from database import database_access as db
from services.calculate_population import calculate_population
from utils.logger import log_trace, log_error

TMPDIR = 'tmp/'

def create_tmp_dir():
	if not os.path.exists(TMPDIR):
		os.makedirs(TMPDIR)

def savefile(filedata):
	create_tmp_dir()
	zip_name = "gtfs_{0}.zip".format(datetime.today().strftime('%Y-%m-%d_%H-%M-%S'))
	zip_path = os.path.join(TMPDIR, zip_name)
	with open(zip_path, 'wb') as f:
		f.write(filedata)
	return zip_path

def add_gtfs_to_db(file):
	dbname = _filename_to_dbname(file)
	db.create_db(dbname)
	dao = db.access_direct_dao(dbname)
	
	errormsg = None
	try:
		log_trace("Creating dataset...")
		dataset_id = db.create_dataset(dbname)
		log_trace("Loading GTFS...")
		dao.load_gtfs(file)
		new_agencies = dao.agencies()
		log_trace("Calculating lat/lng of agencies...")
		lat, lng = db.get_random_mean_lat_lng(dbname)
		log_trace("Updating agencies...")
		old_dataset_ids = db.update_agencies(new_agencies, dataset_id, lat, lng)
		for old_id in old_dataset_ids:
			log_trace("Deleting old dataset...")
			db.delete_dataset(old_id)
		calculate_urban(dbname)
		log_trace("Filling population database...")
		calculate_population(dbname, dataset_id)

		log_trace("Setting success...")
		db.set_done(dataset_id)
		log_trace("Done")
	except Exception as e:
		log_error(e)
		db.set_failed(dataset_id)
		db.drop_database(dbname)
		# TODO delete all created stuff and put db in old state
		raise Exception("Error loading gtfs zip file: {0}".format(str(e)))

	return dbname

def calculate_urban(dbname):
    log_trace("Creating and filling urban table...")
    db.create_and_fill_urban_table(dbname)
    log_trace("Done calculating urban")

def status_of_last_upload():
    done, fail = db.get_last_dataset_status()
    return {"done": done, 
            "failed": fail }

def _filename_to_dbname(filename):
	filename = os.path.basename(filename)
	if filename.endswith(".zip"):
		filename = filename[:-4]
	# Delete punctuation (of created file name)
	return filename.replace('-', '').replace('_', '')
