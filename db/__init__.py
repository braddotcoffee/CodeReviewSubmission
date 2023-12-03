from config import YAMLConfig as Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

ONE_HOUR = 3600

Base = declarative_base()

class DB:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(DB, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self):
        if self.__initialized:
            return

        self.__initialized = True

        username = Config.CONFIG["Database"]["Username"]
        password = Config.CONFIG["Secrets"]["Database"]["Password"]
        db_host = Config.CONFIG["Database"]["Host"]
        db_name = Config.CONFIG["Database"]["Name"]

        self.engine = create_engine(
            f"mysql+pymysql://{username}:{password}@{db_host}/{db_name}",
            pool_recycle=ONE_HOUR,
            pool_pre_ping=True
        )
        self.session = sessionmaker(self.engine, autoflush=True, autocommit=True)

        Base.metadata.create_all(self.engine)