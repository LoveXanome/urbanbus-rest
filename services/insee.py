# -*- coding: utf-8 -*-

import json
import csv
import subprocess
from os import path, rename, makedirs
import requests
import zipfile
from threading import Thread
from utils.logger import log_trace

TMP_DIR = "tmp/"

def get_population(left,bottom,right,top):
	command = "insee-200m-extract.bat --left "+str(left)+" --bottom "+str(bottom)+" --right "+str(right)+" --top "+str(top)+" --csv --outputPrefix INSEE_200m"
	p = subprocess.call(command)
	csvfile = open('INSEE_200m.csv', 'r')
	fieldnames = ("x","y","ind","men","men_surf_sum","men_surf_norm","men_occ5_sum","men_occ5_norm","men_coll_sum","men_coll_norm","men_5ind_sum","men_5ind_norm","men_1ind_sum","men_1ind_norm","men_prop_sum","men_prop_norm","men_basr_sum","men_basr_norm","ind_age1_sum","ind_age1_norm","ind_age2_sum","ind_age2_norm","ind_age3_sum","ind_age3_norm","ind_age4_sum","ind_age4_norm","ind_age5_sum","ind_age5_norm","ind_age6_sum","ind_age6_norm","ind_age7_sum","ind_age7_norm","ind_age8_sum","ind_age8_norm","ind_srf_sum","ind_srf_norm")
	reader = csv.DictReader( csvfile, fieldnames)
	popTot = 0
	for row in reader:
		if row["ind"] != "ind" :
			popTot = popTot + int(float(row["ind"]))	
	return popTot

def download_insee_files():
    if not path.exists(TMP_DIR):
        makedirs(TMP_DIR)
    
    threads = []
    if not path.isfile("car_m.dbf"):
        t = Thread(target=_get_file, args=("200m-carreaux-metropole.zip", "car_m.dbf",))
        threads.append(t)
        t.start()
    else:
        log_trace("car_m.dbf already exists")
    
    if not path.isfile("rect_m.dbf"):
        t = Thread(target=_get_file, args=("200m-rectangles-metropole.zip", "rect_m.dbf",))
        threads.append(t)
        t.start()
    else:
        log_trace("rect_m.dbf already exists")
    
    for t in threads:
        t.join()

def _get_file(zipname, filename):
    dest_zip = path.join(TMP_DIR, zipname)
    # Download
    log_trace("Downloading {0}".format(dest_zip))
    file = requests.get("http://www.insee.fr/fr/ppp/bases-de-donnees/donnees-detaillees/donnees-carroyees/zip/{0}".format(zipname))
    with open(dest_zip, 'wb') as f:
        f.write(file.content)
    # Unzip
    log_trace("Unziping {0}".format(dest_zip))
    with zipfile.ZipFile(dest_zip, 'r') as zip_ref:
        zip_ref.extractall(TMP_DIR)
    # Move
    src = path.join(dest_zip[:-4], filename)
    dest = filename
    log_trace("Moving {0} to {1}".format(src, dest))
    rename(src, dest)
