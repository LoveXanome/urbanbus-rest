# Urban bus - REST

## Init

* `git clone https://github.com/LoveXanome/urbanbus-rest.git`
* `git submodule update --init --recursive`

## Production

* make create a `config.py` like :
```
SQLITE = 1
POSTGRE = 2
DATABASE = POSTGRE

POSTGRE_USER = 'gtfs_user'
POSTGRE_PASS = 'mypass'

SECRET_KEY = 'coucou-hibou'```