# -*- coding: utf-8 -*-

from database.database_access import get_dao
from gtfslib.model import Route, StopTime, Shape
from gtfsplugins import decret_2015_1610
from database.database_access import get_dao

def get_routes_details(limit):
	dao = get_dao()
	parsedRoutes = []
	count = 0
	for route in dao.routes(fltr=Route.route_type == Route.TYPE_BUS):
		if count < limit:
			parsedRoute = dict()
			parsedStops = []
			parsedRoute["name"] = route.route_long_name
			count+=1
			
			# All trips have same trip_id so we may use only the first
			shape = dao.shape(route.trips[0].shape_id)
			parsedPoints = []
			if shape is not None:
				for point in shape.points:
					parsedPoint = dict()
					parsedPoint['lat'] = point.shape_pt_lat
					parsedPoint['lon'] = point.shape_pt_lon
					parsedPoints.append(parsedPoint)
				parsedRoute['points'] = parsedPoints

			# All trips have same trip_id so we may use only the first
			stoptimes = dao.stoptimes(fltr=StopTime.trip_id == route.trips[0].trip_id)
			print "nb of trips: "+str(len(route.trips))
			print "ID trip used: "+str(route.trips[0].trip_id)
			print "trip headsign used: "+route.trips[0].trip_headsign.encode('ASCII', 'ignore')
			#print stoptimes

			for stoptime in stoptimes:
				stop = dao.stop(stoptime.stop_id)
				parsedStop = dict()
				if stop is not None:
					parsedStop['name'] = stop.stop_name
					parsedStop['lat'] = stop.stop_lat
					parsedStop['lng'] = stop.stop_lon
				parsedStops.append(parsedStop)

			parsedRoute['stops'] = parsedStops
			parsedRoutes.append(parsedRoute)

	return parsedRoutes

def get_stoptime():
	pass

