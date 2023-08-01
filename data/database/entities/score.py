from sqlalchemy import Column, Integer, String
from ..declarative_base import Base


class Score(Base):
    """
    This class represents the "score" table in the database.
    Each instance of this class represents a record in the "score" table.
    """
    __tablename__ = 'score'
    id = Column(Integer, primary_key=True)
    infrastructure = Column(Integer)
    proactive = Column(Integer)
    realtime = Column(Integer)
    total = Column(Integer)