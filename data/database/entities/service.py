from sqlalchemy import Column, Integer, String, Boolean
from ..declarative_base import Base


class Service(Base):
    """
    This class represents the "service" table in the database.
    Each instance of this class represents a record in the "service" table.
    """
    __tablename__ = 'service'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    monitored = Column(Boolean)