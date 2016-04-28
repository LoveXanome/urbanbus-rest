from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists
from sqlalchemy.schema import MetaData
from gtfslib import dao

Base = declarative_base()
sessionmaker_default = None

''' Object-Database mapping '''

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

''' "public" functions '''

def init_db():
	engine = create_engine(_get_default_database_name())
	global sessionmaker_default
	sessionmaker_default = sessionmaker(bind=engine)
	Base.metadata.create_all(engine)

def get_dao(agency_id):
	database_name = _retrieve_database(agency_id)
	complete_db_name = _get_complete_database_name(database_name)
	return dao.Dao(complete_db_name)

def get_all_agencies():
	session = _get_default_db_session()
	agencies = []
	for row in session.query(Agency).all():
		agencies.append(row)
	session.close()
	return agencies
	
def access_direct_dao(dbname):
	return dao.Dao(_get_complete_database_name(dbname))	

def create_dataset(dbname):
	session = _get_default_db_session()
	
	new_dataset = Dataset(database_name=dbname)
	session.add(new_dataset)
	session.commit()
	
	new_dataset_id = new_dataset.id
	session.close()
	return new_dataset_id
	
def update_agencies(new_agencies, new_dataset_id):
	session = _get_default_db_session()
	old_ids = []
	for agency in new_agencies:
		if _agency_exist(session, agency.agency_id, agency.agency_name):
			ag = session.query(Agency).filter(Agency.agency_id == agency.agency_id, Agency.agency_name == agency.agency_name)[0]
			old_ids.append(ag.dataset)
			ag.dataset = new_dataset_id
		else:
			session.add(Agency(agency_id=agency.agency_id, agency_name=agency.agency_name, dataset=new_dataset_id))
			
	session.commit()
	session.close()
	return old_ids
	
def delete_dataset(id):
	session = _get_default_db_session()
	
	dataset = session.query(Dataset).filter(Dataset.id == id)[0]
	dbname = dataset.database_name
	drop_database(dbname)
	session.delete(dataset)
	
	session.commit()
	session.close()
	pass
	
def drop_database(dbname):
	engine = create_engine(_get_complete_database_name(dbname))
	meta = MetaData(bind=engine)
	meta.drop_all(checkfirst=False) # TODO doesn't really work. Database still full.

''' "private" functions '''

def _get_default_db_session():
	global sessionmaker_default
	return sessionmaker_default()

def _retrieve_database(agency_id):
	session = _get_default_db_session()
	agencies = []
	for agency in session.query(Agency).filter(Agency.id==agency_id):
		agencies.append(agency)
	if len(agencies) != 1:
		session.close()
		raise Exception('Found {0} agencies instead of one'.format(len(agencies)))
	agency = agencies[0]
	
	datasets = []
	for dataset in session.query(Dataset).filter(Dataset.id==agency.dataset):
		datasets.append(dataset)
	if len(datasets) != 1:
		session.close()
		raise Exception('Found {0} dataset instead of one'.format(len(datasets)))
	dataset = datasets[0]
	
	session.close()
	return dataset.database_name

def _get_default_database_name():
	return _get_complete_database_name("general")

def _get_complete_database_name(database):
	return "sqlite:///database/{0}.sqlite".format(database) # TODO conf file for database

def _agency_exist(session, id, name):
	result = []
	for a in session.query(Agency).filter(Agency.agency_id == id, Agency.agency_name == name):
		result.append(a)
	return len(result) != 0
