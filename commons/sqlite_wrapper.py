import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from commons.db_models import Base
from commons.globals import *

logger = logging.getLogger(LOGGER_NAME)


class SQLiteHelper:

    def __init__(self, db_path):
        _connection_info = 'sqlite:///%s' % db_path
        _engine = create_engine(_connection_info)
        Base.metadata.create_all(_engine)
        self._session = scoped_session(sessionmaker(bind=_engine))


    @property
    def session(self):
        if hasattr(self, '_session'):
            return self._session()
