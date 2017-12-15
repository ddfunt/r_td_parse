from DB.utils import make_temp_session, init_db
from DB.base import Base

DB_NAME = 'TRUMPUSERS'

def check_db():
    session = make_temp_session(DB_NAME)
    print(session)

def startup():
    check_db()
    init_db(DB_NAME)




if __name__ == '__main__':
    startup()
    for session in make_temp_session(DB_NAME):
        session.add(Base())
        session.commit()