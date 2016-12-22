from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
)

from .meta import Base


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    body = Column(Unicode)
    creation_date = Column(Unicode)


Index('my_index', MyModel.title, MyModel.creation_date, MyModel.body, unique=True, mysql_length=255)
