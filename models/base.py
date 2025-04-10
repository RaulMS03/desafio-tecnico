from dotenv import load_dotenv
from peewee import Model
from database.db import db

load_dotenv()

class BaseModel(Model):
    class Meta:
        database = db