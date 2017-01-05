from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    Date,
)

from .meta import Base


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    body = Column(Unicode)
    creation_date = Column(Date)

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "creation_date": self.creation_date
        }
