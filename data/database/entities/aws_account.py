from sqlalchemy import Column, Integer, String
from ..declarative_base import Base
from sqlalchemy.orm import relationship


class AWSAccount(Base):
    """
    This class represents the "aws_account" table in the database.
    Each instance of this class represents a record in the "aws_account" table.
    """
    __tablename__ = 'aws_account'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    environment = Column(String(50))
    organization = Column(String(50))
    # grafana_org = relationship('Organization', back_populates="AWSAccount")
