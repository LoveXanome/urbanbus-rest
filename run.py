# -*- coding: utf-8 -*-

from gtfslib.dao import Dao
from gtfslib.model import Route


dao = Dao("services/db.sqlite")
route=""
print "console log"
routes = dao.routes(fltr=Route.route_type == Route.TYPE_BUS)
route = ("%s: %s %d trips" % (routes[0].route_long_name, str(routes[0].trips), len(routes[0].trips)))
print route
