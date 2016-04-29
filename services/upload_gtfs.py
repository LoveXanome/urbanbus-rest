# -*- coding: utf-8 -*-

from datetime import datetime
import os
from database import database_access as db

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
		dao.load_gtfs(file)
		dataset_id = db.create_dataset(dbname)
		new_agencies = dao.agencies()
		old_dataset_ids = db.update_agencies(new_agencies, dataset_id)
		for old_id in old_dataset_ids:
			db.delete_dataset(old_id)
			
	except Exception as e:
		db.drop_database(dbname)
		# TODO delete all created stuff and put db in old state
		raise Exception("Error loading gtfs zip file: {0}".format(str(e)))
	return dbname

def calculate_urban(dbname):
    db.create_and_fill_urban_table(dbname)


def _filename_to_dbname(filename):
	filename = os.path.basename(filename)
	if filename.endswith(".zip"):
		filename = filename[:-4]
	# Delete punctuation (of created file name)
	return filename.replace('-', '').replace('_', '')
