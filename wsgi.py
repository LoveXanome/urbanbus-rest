import sys
import os

gtfslibpath = os.path.join(os.getcwd(), 'gtfslib-python')
sys.path.append(gtfslibpath)

from database.database_access import init_db
init_db()

import config
from app import app as application
application.secret_key = config.SECRET_KEY

if __name__ == "__main__":
    application.run()
