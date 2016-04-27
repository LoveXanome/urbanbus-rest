from gtfslib.dao import Dao

# TODO : adaptable configuration for database

def get_dao():
	return dao.Dao('database/db.sqlite')
