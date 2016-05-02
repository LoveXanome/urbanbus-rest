from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, func, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists
from sqlalchemy.schema import MetaData
from gtfslib import dao
from gtfsplugins.decret_2015_1610 import decret_2015_1610
from random import randint
import config
from os import remove

Base = declarative_base()
GtfsBase = declarative_base()
sessionmaker_default = None

''' Object-Database mapping '''

class Dataset(Base):
	__tablename__ = 'dataset'
	__table_args__ = {'useexisting': True, 'sqlite_autoincrement': True}
	
	id = Column(Integer, primary_key=True, nullable=False)
	database_name = Column(String, nullable=False)
	add_date = Column(DateTime, default=func.now(), nullable=False)
	upload_success = Column(Boolean, nullable=False, default=False)
	upload_failed = Column(Boolean, nullable=False, default=False)
	
	def __repr__(self):
		return "<Dataset(id='{0}', database_name='{1}', add_date='{2}', upload_success='{3}', upload_failed='{4}')>".format(self.id, self.database_name, self.add_date, self.upload_success, self.upload_failed)
	
class Agency(Base):
	__tablename__ = 'agency'
	__table_args__ = {'useexisting': True, 'sqlite_autoincrement': True}
	
	id = Column(Integer, primary_key=True, nullable=False)
	agency_id = Column(String, nullable=False)
	agency_name = Column(String, nullable=False)
	latitude = Column(Float, nullable=False)
	longitude = Column(Float, nullable=False)
	dataset = Column(Integer, ForeignKey('dataset.id'))
	
	def __repr__(self):
		return "<Agency(id='{0}', agency_id='{1}', agency_name='{2}', dataset='{3}')>".format(self.id, self.agency_id, self.agency_name, self.dataset)

class Urban(GtfsBase):
    __tablename__ = 'urban'
    __table_args__ = {'useexisting': True, 'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True, nullable=False)
    category = Column(Boolean, nullable=True)
    route = Column(String, nullable=False, unique=True) # TODO ForeignKey on mapper in gtfslib.orm

    def __repr__(self):
        return "<Urban(id='{0}', category='{1}', route='{2}')>".format(self.id, self.category, self.route)

class Population(Base) :
	__tablename__ = 'population'
	__table_args__ = {'useexisting': True, 'sqlite_autoincrement': True}

	id = Column(Integer, primary_key=True, nullable=False)
	agency_id = Column(String, nullable=False)
	stop_id = Column(String, nullable=False)
	population = Column(Integer, nullable=True)
	
	def __repr__(self):
		return "<Population(agency_id='{0}', stop_id='{1}', population='{2}')>".format(self.id, self.category, self.route)

''' "public" functions '''

def init_db():
    _database_op("general", create=True)

    engine = create_engine(_get_default_database_name())
    global sessionmaker_default
    sessionmaker_default = sessionmaker(bind=engine)
    global Base
    try:
        Base.metadata.create_all(engine)
    except:
        pass

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

def get_agency_by_id(agency_id):
    session = _get_default_db_session()
    agencies = []
    for row in session.query(Agency).filter(Agency.id==agency_id):
        agencies.append(row)
    session.close()
    return agencies[0]

def create_db(dbname):
    _database_op(dbname, create=True)

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

def set_success(dataset_id):
    session = _get_default_db_session()
    dataset = None
    for d in session.query(Dataset).filter(Dataset.id==dataset_id):
        dataset = d
        break
    if not dataset:
        raise Exception("Could not find dataset with id {0}".format(dataset_id))
    dataset.upload_success = True
    session.commit()
    session.close()

def set_failed(dataset_id):
    session = _get_default_db_session()
    dataset = None
    for d in session.query(Dataset).filter(Dataset.id==dataset_id):
        dataset = d
        break
    if not dataset:
        raise Exception("Could not find dataset with id {0}".format(dataset_id))
    dataset.upload_failed = True
    session.commit()
    session.close()

def get_last_dataset_status():
    session = _get_default_db_session()
    succ = False
    fail = False
    for d in session.query(Dataset).order_by(Dataset.id.desc()):
        succ = d.upload_success
        fail = d.upload_failed
        break
    session.commit()
    session.close()
    return succ, fail

def update_agencies(new_agencies, new_dataset_id, lat, lng):
	session = _get_default_db_session()
	old_ids = []
	for agency in new_agencies:
		if _agency_exist(session, agency.agency_id, agency.agency_name):
			ag = session.query(Agency).filter(Agency.agency_id == agency.agency_id, Agency.agency_name == agency.agency_name)[0]
			old_ids.append(ag.dataset)
			ag.dataset = new_dataset_id
			ag.latitude = lat
			ag.longitude = lng
		else:
			session.add(Agency( agency_id=agency.agency_id,
                                agency_name=agency.agency_name,
                                latitude=lat,
                                longitude=lng,
                                dataset=new_dataset_id))
			
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

def get_random_mean_lat_lng(dbname):
    engine = create_engine(_get_complete_database_name(dbname))
    selected = []
    nb_points = 1
    with engine.connect() as con:
        sql_result = con.execute("SELECT * FROM shape_pts")
        results = []

        for r in sql_result:
            results.append(r)
  
        nb_points = min(len(results), 50)
        for i in range(nb_points):
            rand_i = randint(0, len(results)-1)
            selected.append(results[rand_i])

    if nb_points == 0:
        return 0, 0
    lat = 0.
    long = 0.
    for r in selected:
        lat += r[4]
        long += r[5]
    lat /= nb_points
    long /= nb_points

    return lat, long

def get_lat_lng(agency_id):
    session = _get_default_db_session()
    lat = 0
    lng = 0
    for r in session.query(Agency).filter(Agency.id==agency_id):
        lat = r.latitude
        lng = r.longitude
        break
    session.close()
    return {'lat': lat, 'lng': lng}

def drop_database(dbname):
    _database_op(dbname, create=False, drop=True)

# Functions for urban table
def create_and_fill_urban_table(dbname):
    full_dbname = _get_complete_database_name(dbname)
    engine = _create_urban_table(full_dbname)
    sessionmk = sessionmaker(bind=engine)
    session = sessionmk()

    dbdao = dao.Dao(full_dbname)
    for route in dbdao.routes(prefetch_trips=True):
        urban = _is_urban(route)
        _insert_urban(session, route.route_id, urban)
    session.close()

def get_urban(agency_id):
    database_name = _retrieve_database(agency_id)
    complete_db_name = _get_complete_database_name(database_name)
    engine = create_engine(complete_db_name)
    sessionmk = sessionmaker(bind=engine)
    session = sessionmk()

    urban_result = {}
    for urb in session.query(Urban).all():
        urban_result[urb.route] = urb.category
    session.close()
    return urban_result

def get_urban_by_id(agency_id, route_id):
    database_name = _retrieve_database(agency_id)
    complete_db_name = _get_complete_database_name(database_name)
    engine = create_engine(complete_db_name)
    sessionmk = sessionmaker(bind=engine)
    session = sessionmk()

    urban_result = []
    for urb in session.query(Urban).filter(Urban.route==route_id):
        urban_result.append(urb)
    session.close()
    return urban_result[0].category
	
# Functions for population table	
def fill_population_table(agency_id, stop_id, population):
    session = _get_default_db_session()
    _insert_population(agency_id, stop_id, population)
    session.close()
	
def get_population(agency_id):
    session = _get_default_db_session()

    population_result = {}
    for pop in session.query(Population).filter(Population.agency_id==agency_id):
        population_result['stop_id'] = pop.population
    session.close()
    return population_result
	
def get_population_by_id(agency_id, stop_id):
    session = _get_default_db_session()

    population_result = []
    for pop in session.query(Population).filter(Population.agency_id==agency.id, Population.stop_id==stop_id):
        population_result.append(pop)
    session.close()
    return population_result[0].population
	
	
    lat = 0
    lng = 0
    for r in session.query(Agency).filter(Agency.id==agency_id):
        lat = r.latitude
        lng = r.longitude
        break
    session.close()
    return {'lat': lat, 'lng': lng}

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
    if config.DATABASE == config.POSTGRE:
        return "postgresql://{0}:{1}@{2}/{3}".format(config.POSTGRE_USER, config.POSTGRE_PASS, config.POSTGRE_HOST, database)
    if config.DATABASE == config.SQLITE:
        return "sqlite:///database/{0}.sqlite".format(database)


def _agency_exist(session, id, name):
	result = []
	for a in session.query(Agency).filter(Agency.agency_id == id, Agency.agency_name == name):
		result.append(a)
	return len(result) != 0


def _is_urban(route):
    return decret_2015_1610(route.trips, False)

def _create_urban_table(full_dbname):
    engine = create_engine(full_dbname)
    GtfsBase.metadata.create_all(engine)
    return engine


def _insert_urban(session, route_id, is_urban):
    u = Urban(route=route_id, category=is_urban)
    session.add(u)
    session.commit()
	
def _insert_population(agency_id,stop_id, population):
    p = Population(agency_id=agency_id, stop_id=stop_id, population=population)
    session.add(p)
    session.commit()
	
	

def _database_op(dbname, create=True, drop=False):
    if config.DATABASE == config.POSTGRE:
        db_engine = create_engine(_get_complete_database_name("postgres"))
        connection = db_engine.connect()
        connection.execute("commit")
        try:
            if create:
                connection.execute('CREATE DATABASE "{0}"'.format(dbname))
            if drop:
                connection.execute('DROP DATABASE "{0}"'.format(dbname))
        except:
            pass
        connection.close()
    elif config.DATABASE == config.SQLITE:
        if create:
            create_engine(_get_complete_database_name(dbname))
        if drop:
            remove("database/{0}.sqlite".format(dbname))
