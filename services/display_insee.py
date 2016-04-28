# -*- coding: utf-8 -*-

import json
import csv
import subprocess


def get_insee():
	#p = subprocess.Popen(['start','insee-200m-extract.bat','--left','5.23','--bottom','43.16','--right','5.58','--top','43.40','--csv','--outputPrefix','INSEE_200m'])
	#p = subprocess.Popen(["insee-200m-extract.bat --left 5.23 --bottom 43.16 --right 5.58 --top 43.40 --csv --outputPrefix INSEE_200m"])
	p = subprocess.call("insee-200m-extract.bat --left 5.23 --bottom 43.16 --right 5.58 --top 43.40 --csv --outputPrefix INSEE_200m",creationflags=subprocess.CREATE_NEW_CONSOLE)
	csvfile = open('INSEE_200m.csv', 'r')
	jsonfile = open('INSEE_200m.json', 'w')
	fieldnames = ("x","y","ind","men","men_surf_sum","men_surf_norm","men_occ5_sum","men_occ5_norm","men_coll_sum","men_coll_norm","men_5ind_sum","men_5ind_norm","men_1ind_sum","men_1ind_norm","men_prop_sum","men_prop_norm","men_basr_sum","men_basr_norm","ind_age1_sum","ind_age1_norm","ind_age2_sum","ind_age2_norm","ind_age3_sum","ind_age3_norm","ind_age4_sum","ind_age4_norm","ind_age5_sum","ind_age5_norm","ind_age6_sum","ind_age6_norm","ind_age7_sum","ind_age7_norm","ind_age8_sum","ind_age8_norm","ind_srf_sum","ind_srf_norm")
	reader = csv.DictReader( csvfile, fieldnames)
	for row in reader:
		json.dump(row, jsonfile)
		jsonfile.write('\n')
	jsonfile.close()
	
	data = []
	with open('INSEE_200m.json') as f:
		for line in f:
			data.append(json.loads(line))
	f.close()
	return data