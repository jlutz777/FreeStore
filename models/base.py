from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

import os

Base = declarative_base()
postgresConn = os.environ.get("POSTGRES_CONN", "")
engine = create_engine(postgresConn)
