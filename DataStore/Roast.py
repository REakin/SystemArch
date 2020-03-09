from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class Roast(Base):
    """Region"""

    __tablename__ = "Roast"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    region = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, ids, name, region):
        self.id = ids
        self.name = name
        self.region = region
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        dict = {}
        dict['id'] = self.id
        dict['name'] = self.name
        dict['region'] = self.region

        return dict