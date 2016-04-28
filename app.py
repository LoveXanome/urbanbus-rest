# -*- coding: utf-8 -*-
import sys, os

gtfslibpath = os.path.join(os.getcwd(), 'gtfslib-python')
sys.path.append(gtfslibpath)

from flask import Flask, request, abort
from services import upload_gtfs
from services.display_routes import get_routes
from services.display_agencies import get_agencies
from database.database_access import init_db
import json

app = Flask(__name__)

def error(message):
    return json.dumps({"error": message})

@app.route("/agencies", methods=['GET'])
def display_agencies():
	return get_agencies()

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

@app.route("/agencies/<int:agency_id>/routes", methods=['GET'])
def display_routes(agency_id):
    try:
        return get_routes(agency_id)
    except Exception as e:
        return error(str(e))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
