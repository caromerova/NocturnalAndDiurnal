from config.database import Base
from sqlalchemy import Column, Integer, String

class Vehicles(Base):

    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    plate = Column(String, nullable=False)
    overview = Column(String, nullable=False)
    model = Column(Integer, nullable=False)
    type = Column(String, nullable=False)
    category = Column(String, nullable=False)
