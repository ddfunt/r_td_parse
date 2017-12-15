from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


def make_temp_session(db_name, ):
    engine = create_engine('sqlite:///'.format(db_name))
    engine.connect()
    session = Session(bind=engine)
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


def init_db(db_name):
    for session in make_temp_session(db_name):
        session.commit()
    #for session

