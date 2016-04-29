import sys
import os

sys.path.insert(0, '/var/www/urbanbus-rest/')
sys.path.append('/var/www/urbanbus-rest/gtfslib-python/')

from database.database_access import init_db
init_db()

from app import app as application
application.secret_key = 'COUCOU_HIBOU'

