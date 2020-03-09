from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class Region(Base):
    """Region"""

    __tablename__ = "Region"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    date_created = (Column(DateTime, nullable=False))

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        dict = {}
        dict['id'] = self.id
        dict['name'] = self.name

        return dict