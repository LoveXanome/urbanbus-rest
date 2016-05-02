# -*- coding: utf-8 -*-
import sys, os

gtfslibpath = os.path.join(os.getcwd(), 'gtfslib-python')
sys.path.append(gtfslibpath)

from flask import Flask, request, abort, jsonify
from flask.ext.cors import CORS

from database.database_access import init_db

from services import upload_gtfs
from services.service_handler import call_service
from services.get_agencies import get_agencies
from services.get_agency import get_agency
from services.get_routes import get_routes
from services.get_route import get_route
from utils.logger import log_error
from threading import Thread


app = Flask(__name__)
CORS(app)

def error(message):
    return jsonify({"error": message}), 400

''' UPLOAD endpoints '''

# Example: curl -i -H "Content-Type: application/octet-stream" -X POST --data-binary @nantes.zip http://localhost:5000/upload/gtfs
@app.route("/upload/gtfs", methods=['PUT', 'POST'])
def upload_file():
    if request.headers['Content-Type'] != 'application/octet-stream':
        abort(400)
    filename = upload_gtfs.savefile(request.data)

    # Launch bg task for adding gtfs to database
    thread = Thread(target=upload_file_thread, args=(filename,))
    thread.start()

    # TODO Launch bg task for calculating population per stop

    return jsonify({"status": 201}), 201

def upload_file_thread(filename):
    try:
        database_name = upload_gtfs.add_gtfs_to_db(filename)
        # Urban calcul made in function above
    except Exception as e:
        log_error(e)
        return error(str(e))

@app.route("/upload/status", methods=['GET'])
def upload_status():
    return jsonify({"status": upload_gtfs.status_of_last_upload()}), 200

''' GET endpoints '''

@app.route("/agencies", methods=['GET'])
def display_agencies():
    return call_service(get_agencies, "agencies")


@app.route("/agencies/<int:agency_id>", methods=['GET'])
def display_agency(agency_id):
    params = { 'agency_id': agency_id }
    return call_service(get_agency, "agency", **params)


@app.route("/agencies/<int:agency_id>/routes", methods=['GET'])
def display_routes(agency_id):
    params = { 'agency_id': agency_id }
    return call_service(get_routes, "routes", **params)


@app.route("/agencies/<int:agency_id>/routes/<route_id>", methods=['GET'])
def display_route(agency_id, route_id):
    params = { 'agency_id': agency_id, 'route_id': route_id }
    return call_service(get_route, "route", **params)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
