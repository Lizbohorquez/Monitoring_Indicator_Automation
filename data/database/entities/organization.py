from sqlalchemy import Column, Integer, String, ForeignKey
from ..declarative_base import Base


class Organization(Base):
    """
    This class represents the "organization" table in the database.
    Each instance of this class represents a record in the "organization" table.
    """
    __tablename__ = 'organization'
    id = Column(Integer, primary_key=True)
    aws_account = Column(Integer, ForeignKey('aws_account.id'), primary_key=True)
    grafana_folder = Column(String)
