# -*- coding: utf-8 -*-
import sys, os

gtfslibpath = os.path.join(os.getcwd(), 'gtfslib-python')
sys.path.append(gtfslibpath)

from flask import Flask, request, abort, jsonify
from services import upload_gtfs
from services.display_routes import get_routes
from services.display_agencies import get_agencies
from services.display_insee import get_insee
import json
from services.check_urban import get_urban_status

app = Flask(__name__)

def error(message):
    return json.dumps({"error": message})

@app.route("/", methods=['POST'])
def upload_gtfszip():
    #print(request, flush=True)
    if not request.json and not 'file' in request.json:
        abort(400)
    file=request.json['file']
    return file


# Example curl -i -H "Content-Type: application/octet-stream" -X POST --data-binary @nantes.zip http://localhost:5000/upload/gtfs
@app.route("/upload/gtfs", methods=['PUT', 'POST'])
def upload_file():
    if request.headers['Content-Type'] != 'application/octet-stream':
        abort(400)
    filename = upload_gtfs.savefile(request.data)
    errormsg = upload_gtfs.add_gtfs_to_db(filename)
    
    if errormsg:
        return error(errormsg), 400
    
    return json.dumps({"status": 201}), 201 

@app.route("/insee", methods=['GET'])
def display_insee():
	return jsonify({ "population": get_insee()})
	
@app.route("/agencies", methods=['GET'])
def display_agencies():
	return jsonify({ "agencies": get_agencies()})

@app.route("/agencies/<int:agency_id>/routes", methods=['GET'])
def display_routes(agency_id):
    return jsonify({ "routes": get_routes()})


@app.route("/agencies/<int:agency_id>/routes/urban", methods=['GET'])
def display_urban(agency_id):
    return jsonify({ "routes": get_urban_status()})


if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True)
