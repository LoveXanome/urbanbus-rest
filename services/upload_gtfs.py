# -*- coding: utf-8 -*-

from datetime import datetime
import os
from database import database_access 

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
	dao = database_access.get_dao()
	errormsg = None
	try:
		dao.load_gtfs(file)
		# TODO add to our table when the file was added
	except Exception as e:
		errormsg = "Error loading gtfs zip file: {0}".format(str(e))
	return errormsg
