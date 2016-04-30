# -*- coding: utf-8 -*-
import sys, os

gtfslibpath = os.path.join(os.getcwd(), 'gtfslib-python')
sys.path.append(gtfslibpath)

from flask import Flask, request, abort, jsonify
from flask.ext.cors import CORS

from utils.timer import get_time
from utils.logger import log_performance

from database.database_access import init_db

from services import upload_gtfs
from services.display_routes import get_routes
from services.display_agencies import get_agencies
from services.check_urban import get_urban_status
from services.display_routes_details import get_routes_details
from services.display_route_details import get_route_details
from services.get_route import get_route



app = Flask(__name__)
CORS(app)

def error(message):
    return jsonify({"error": message}), 400

@app.route("/agencies", methods=['GET'])
def display_agencies():
	return jsonify({"agencies": get_agencies()})

# Example curl -i -H "Content-Type: application/octet-stream" -X POST --data-binary @nantes.zip http://localhost:5000/upload/gtfs
@app.route("/upload/gtfs", methods=['PUT', 'POST'])
def upload_file():
    if request.headers['Content-Type'] != 'application/octet-stream':
        abort(400)
    filename = upload_gtfs.savefile(request.data)
    try:
        database_name = upload_gtfs.add_gtfs_to_db(filename)
        upload_gtfs.calculate_urban(database_name)
    except Exception as e:
        return error(str(e))

    return jsonify({"status": 201}), 201

@app.route("/agencies/<int:agency_id>/routes", methods=['GET'])
def display_routes(agency_id):
    # try:
    #     return jsonify({'data': get_routes(agency_id, 2)})
    # except Exception as e:
    #     return error(str(e))
    return jsonify({'data': get_routes(agency_id)})
    
@app.route("/agencies/<int:agency_id>/routes/urban", methods=['GET'])
def display_urban(agency_id):
    start = get_time()
    try:
        routes = get_urban_status(agency_id)
        nbRoutes = len(routes)
        response = jsonify({ "routes": routes})
    except Exception as e:
        response = error(str(e))
    finally:
        end = get_time()
        params = "| nb routes = "+str(nbRoutes)+" | endpoint = /routes/urban"
        log_performance(start, end, params, "performance.log")
        return response

@app.route("/agencies/<int:agency_id>/routes/details", methods=['GET'])
def display_details(agency_id):
    # try:
    #     return jsonify({ "routes": get_routes_details(agency_id, 6)})
    # except Exception as e:
    #     return error(str(e))
    return jsonify({ "routes": get_routes_details(agency_id, 6)})
	
@app.route("/agencies/<int:agency_id>/routes/<int:route_id>", methods=['GET'])
def display_detailsRoute(agency_id,route_id):
    # try:
    #     return jsonify({ "route": get_route_detail(agency_id,route_id)})
    # except Exception as e:
    #     return error(str(e))
    #return jsonify({ "route": get_route_details(agency_id,route_id)})
    return jsonify({ "route": get_route(agency_id, route_id)})


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
