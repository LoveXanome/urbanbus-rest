# Urban bus - REST

## Init

* `git clone https://github.com/LoveXanome/urbanbus-rest.git`
* `git submodule update --init --recursive`

## Production

* make create a `config.py` like :
```
SQLITE = 1
POSTGRE = 2
DATABASE = SQLITE

POSTGRE_USER = 'gtfs_user'
POSTGRE_PASS = 'mypass'
POSTGRE_HOST = 'localhost'

SECRET_KEY = 'coucou-hibou'

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
