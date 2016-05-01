# Urban bus - REST

## Init

* `git clone https://github.com/LoveXanome/urbanbus-rest.git`
* `git submodule update --init --recursive`

Download these two folders : 
http://www.insee.fr/fr/ppp/bases-de-donnees/donnees-detaillees/donnees-carroyees/zip/200m-carreaux-metropole.zip
http://www.insee.fr/fr/ppp/bases-de-donnees/donnees-detaillees/donnees-carroyees/zip/200m-rectangles-metropole.zip
Unzip them and then place 'car_m.dbf' and 'rect_m.dbf' in the root folder; with 'app.py'.

## Production

* make create a `config.py` like :
```
SQLITE = 1
POSTGRE = 2
DATABASE = SQLITE

POSTGRE_USER = 'gtfs_user'
POSTGRE_PASS = 'mypass'

SECRET_KEY = 'coucou-hibou'

LOG_PERF = False
PRINT_PERF = False
```
## List of endpoints
### [GET] /agencies
To list all agencies available

### [GET] /agencies/agency_id
To get details about an agency

### [GET] /agencies/agency_id/routes
To list all routes available for a given agency

### [GET] /agencies/agency_id/routes/<route_id>
To get details about a particular route
