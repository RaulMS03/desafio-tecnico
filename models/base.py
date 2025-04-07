from dotenv import load_dotenv
from peewee import Model
from database.db import get_postgres_database

load_dotenv()
db = get_postgres_database()

class BaseModel(Model):
    class Meta:
        database = db