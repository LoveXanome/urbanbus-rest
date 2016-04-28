from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from gtfslib import dao

Base = declarative_base()
sessionmaker_default = None

class Dataset(Base):
	__tablename__ = 'dataset'
	__table_args__ = {'useexisting': True, 'sqlite_autoincrement': True}
	
	id = Column(Integer, primary_key=True, nullable=False)
	database_name = Column(String, nullable=False)
	add_date = Column(DateTime, default=func.now(), nullable=False)
	
	def __repr__(self):
		return "<Dataset(id='{0}', database_name='{1}', add_date='{2}')>".format(self.id, self.database_name, self.add_date)
	
class Agency(Base):
	__tablename__ = 'agency'
	__table_args__ = {'useexisting': True, 'sqlite_autoincrement': True}
	
	id = Column(Integer, primary_key=True, nullable=False)
	agency_id = Column(String, nullable=False)
	agency_name = Column(String, nullable=False)
	dataset = Column(Integer, ForeignKey('dataset.id'))
	
	def __repr__(self):
		return "<Agency(id='{0}', agency_id='{1}', agency_name='{2}', dataset='{3}')>".format(self.id, self.agency_id, self.agency_name, self.dataset)


def init_db():
	engine = create_engine(_get_default_database_name())
	global sessionmaker_default
	sessionmaker_default = sessionmaker(bind=engine)
	Base.metadata.create_all(engine)

def get_dao(agencyid):
	database_name = _retrieve_database(agencyid)
	complete_db_name = _get_complete_database_name(database_name)
	return dao.Dao(complete_db_name)

def get_all_agencies():
	session = _get_default_db_session()
	agencies = []
	for row in session.query(Agency).all():
		agencies.append(row)
	session.close()
	return agencies

def _get_default_db_session():
	global sessionmaker_default
	return sessionmaker_default()

def _retrieve_database(agencyid):
	db_name = _get_complete_database_name()

def _get_default_database_name():
	return _get_complete_database_name("general")

def _get_complete_database_name(database):
	return "sqlite:///database/{0}.sqlite".format(database) # TODO conf file for database
