# -*- coding: utf-8 -*-

import json
import csv
import subprocess
from os import path, rename, makedirs
import requests
import zipfile
from threading import Thread
from utils.logger import log_trace

def get_population(left,bottom,right,top):
	command = "insee-200m-extract.bat --left "+str(left)+" --bottom "+str(bottom)+" --right "+str(right)+" --top "+str(top)+" --csv --outputPrefix INSEE_200m"
	p = subprocess.call(command)
	csvfile = open('INSEE_200m.csv', 'r')
	fieldnames = ("x","y","ind","men","men_surf_sum","men_surf_norm","men_occ5_sum","men_occ5_norm","men_coll_sum","men_coll_norm","men_5ind_sum","men_5ind_norm","men_1ind_sum","men_1ind_norm","men_prop_sum","men_prop_norm","men_basr_sum","men_basr_norm","ind_age1_sum","ind_age1_norm","ind_age2_sum","ind_age2_norm","ind_age3_sum","ind_age3_norm","ind_age4_sum","ind_age4_norm","ind_age5_sum","ind_age5_norm","ind_age6_sum","ind_age6_norm","ind_age7_sum","ind_age7_norm","ind_age8_sum","ind_age8_norm","ind_srf_sum","ind_srf_norm")
	reader = csv.DictReader(csvfile, fieldnames)
	popTot = 0
	for row in reader:
		if row["ind"] != "ind":
			popTot = popTot + int(float(row["ind"]))	
	return popTot

def get_population_insee(lat, lng, dist):
	distDegree = dist * 0.0001 / 7.89 #Conversion des mètres en degrés
	left = lng - distDegree
	right = lng + distDegree
	top = lat + distDegree
	bottom = lat - distDegree
	if left > right :
		left = right
		right = lng + distDegree
	if bottom > top :
		top = bottom
		bottom = lat + distDegree
	return get_population(left,bottom,right,top)