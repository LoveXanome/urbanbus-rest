# -*- coding: utf-8 -*-
import sys, os

gtfslibpath = os.path.join(os.getcwd(), 'gtfslib-python')
sys.path.append(gtfslibpath)

from flask import Flask, request, abort, jsonify
from services import upload_gtfs
from services.display_routes import get_routes
from services.display_agencies import get_agencies
from database.database_access import init_db
from services.display_insee import get_insee
from services.check_urban import get_urban_status
from services.display_routes_details import get_routes_details
from flask.ext.cors import CORS

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
    errormsg = upload_gtfs.add_gtfs_to_db(filename)
    
    if errormsg:
        return error(errormsg)
    
    return jsonify({"status": 201}), 201 


@app.route("/agencies/<int:agency_id>/routes", methods=['GET'])
def display_routes(agency_id):
    try:
        return jsonify({'data': get_routes(agency_id)})
    except Exception as e:
        return error(str(e))

@app.route("/agencies/<int:agency_id>/routes/urban", methods=['GET'])
def display_urban(agency_id):
    try:
        return jsonify({ "routes": get_urban_status(agency_id)})
    except Exception as e:
        return error(str(e))

@app.route("/agencies/<int:agency_id>/routes/details", methods=['GET'])
def display_details(agency_id):
    # try:
    #     return jsonify({ "routes": get_routes_details(agency_id, 6)})
    # except Exception as e:
    #     return error(str(e))
    return jsonify({ "routes": get_routes_details(agency_id, 6)})


@app.route("/insee", methods=['GET'])
def display_insee():
	return jsonify({ "population": get_insee()})


if __name__ == "__main__":
    init_db()
    #app.run(host='0.0.0.0', debug=True)
    app.run(debug=True)
