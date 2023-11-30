from config import YAMLConfig as Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import OperationalError

Base = declarative_base()

class DB:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(DB, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def make_db(self):
        self.engine = create_engine(
            f"mysql+pymysql://{self.username}:{self.password}@{self.db_host}/{self.db_name}",
        )
        self.session = sessionmaker(self.engine, autoflush=True, autocommit=True)

        Base.metadata.create_all(self.engine)

    def __init__(self):
        if self.__initialized:
            return

        self.__initialized = True

        self.username = Config.CONFIG["Database"]["Username"]
        self.password = Config.CONFIG["Secrets"]["Database"]["Password"]
        self.db_host = Config.CONFIG["Database"]["Host"]
        self.db_name = Config.CONFIG["Database"]["Name"]

        self.make_db()
    
    def get_session(self):
        try:
            session = self.session()
            session.execute("SELECT 1")
            return session
        except OperationalError:
            self.engine.dispose()
            self.make_db()

            return self.session()            
