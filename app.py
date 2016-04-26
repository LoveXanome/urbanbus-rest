# -*- coding: utf-8 -*-

from flask import Flask, request, abort
from services import upload_gtfs
from services.display_routes import get_routes

app = Flask(__name__)

@app.route("/", methods=['POST'])
def upload_gtfszip():
    print(request, flush=True)
    if not request.json and not 'file' in request.json:
        abort(400)
    file=request.json['file']
    return file
    
@app.route("/upload/gtfs", methods=['PUT', 'POST'])
def upload_file():
    if request.headers['Content-Type'] != 'application/octet-stream':
        abort(400)
    filename = upload_gtfs.savefile(request.data)
    could_add_to_db = upload_gtfs.add_gtfs_to_db(filename)
    
    '''zip_name = "./tmp/gtfs_{0}.zip".format()
    with open('./tmp/gtfs.zip', 'wb') as f:
        f.write(request.data)'''
    return "Binary message written!" # TODO return json saying OK + return code 


@app.route("/routes", methods=['GET'])
def display():
    return get_routes()


if __name__ == "__main__":
    app.run(debug=True)
