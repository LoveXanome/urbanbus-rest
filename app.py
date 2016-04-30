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
from services.service_handler import call_service
from services.get_agencies import get_agencies
from services.display_routes import get_routes
from services.get_route import get_route
from services.display_route_details import get_route_details


app = Flask(__name__)
CORS(app)

def error(message):
    return jsonify({"error": message}), 400


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


''' GET endpoints '''

@app.route("/agencies", methods=['GET'])
def display_agencies():
    return call_service(get_agencies, "agencies")


@app.route("/agencies/<int:agency_id>/routes", methods=['GET'])
def display_routes(agency_id):
    params = { 'agency_id': agency_id, 'limit': 2 }
    return call_service(get_routes, "data", **params)

	
@app.route("/agencies/<int:agency_id>/routes/<int:route_id>", methods=['GET'])
def display_route(agency_id, route_id):
    params = { 'agency_id': agency_id, 'route_id': route_id }
    return call_service(get_route, "route", **params)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
