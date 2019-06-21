import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from commons.db_models import Base
from globals import *

logger = logging.getLogger(LOGGER_NAME)


class SQLiteHelper:

    def __init__(self, db_path):
        _connection_info = f'sqlite://{db_path}'
        _engine = create_engine(_connection_info)
        self._session = sessionmaker(bind=_engine)
        Base.metadata.create_all(_engine)

    @property
    def session(self):
        if hasattr(self, '_session'):
            return self._session
