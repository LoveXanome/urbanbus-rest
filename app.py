# -*- coding: utf-8 -*-
import sys, os

gtfslibpath = os.path.join(os.getcwd(), 'gtfslib-python')
sys.path.append(gtfslibpath)

from flask import Flask, request, abort
from services import upload_gtfs
from services.display_routes import get_routes
from services.display_agencies import get_agencies

app = Flask(__name__)

@app.route("/", methods=['POST'])
def upload_gtfszip():
    print(request, flush=True)
    if not request.json and not 'file' in request.json:
        abort(400)
    file=request.json['file']
    return file


# curl -i -H "Content-Type: application/octet-stream" -X POST --data-binary @C:\\Users\\David\\Documents\\PLD-SmartCity\\urbanbus-rest\\requirements.txt http://localhost:5000/upload/gtfs    
@app.route("/upload/gtfs", methods=['PUT', 'POST'])
def upload_file():
    if request.headers['Content-Type'] != 'application/octet-stream':
        abort(400)
    filename = upload_gtfs.savefile(request.data)
    could_add_to_db = upload_gtfs.add_gtfs_to_db(filename)
    
    return filename # TODO return json saying OK + return code 

@app.route("/agencies", methods=['GET'])
def display_agencies():
	return get_agencies()

@app.route("/routes", methods=['GET'])
def display():
    return get_routes()


if __name__ == "__main__":
    app.run(debug=True)
