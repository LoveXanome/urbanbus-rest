# Urban bus - REST

## Init

Clone the repository and its submodules :
* `git clone https://github.com/LoveXanome/urbanbus-rest.git`
* `git submodule update --init --recursive`

Then, download these two files, unzip them and place `car_m.dbf` and `rect_m.dbf` in the root folder; with `app.py` :
* http://www.insee.fr/fr/ppp/bases-de-donnees/donnees-detaillees/donnees-carroyees/zip/200m-carreaux-metropole.zip
* http://www.insee.fr/fr/ppp/bases-de-donnees/donnees-detaillees/donnees-carroyees/zip/200m-rectangles-metropole.zip


## Production

* make create a `config.py` like :
```
import os

SQLITE = 1
POSTGRE = 2
DATABASE = os.environ.get('DATABASE') or SQLITE

POSTGRE_USER = os.environ.get('POSTGRE_USER') or 'gtfs_user'
POSTGRE_PASS = os.environ.get('POSTGRE_PASS') or 'mypass'
POSTGRE_HOST = os.environ.get('POSTGRE_HOST') or 'localhost'

SECRET_KEY = os.environ.get('SECRET_KEY') or 'coucou-hibou'

LOG_PERF = False
PRINT_PERF = False
```

## List of endpoints
### [GET] /agencies
To list all agencies available

### [GET] /agencies/agency_id
To get details about an agency (agency_id is an integer)

### [GET] /agencies/agency_id/routes
To list all routes available for a given agency

### [GET] /agencies/agency_id/routes/route_id
To get details about a particular route (route_id is a string)
