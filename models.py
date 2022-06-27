from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Forecast(Base):
    __tablename__ = "forecast"

    id = Column(Integer, primary_key=True)
    parameter = Column(String, nullable=False)
    value = Column(String, nullable=False)
    unit = Column(String, nullable=False)
    source = Column(String, nullable=False)
    valid_time = Column(DateTime, nullable=False)
    retrieved_time = Column(DateTime, nullable=False)
    days_forecasted = Column(Integer, nullable=False)

    def __repr__(self):
        return f"Forecast(parameter={self.parameter}, value={self.value}, source={self.source}, retrieved_time={self.retrieved_time}, days_forecasted={self.days_forecasted})"


class Observation(Base):
    __tablename__ = "observation"

    id = Column(Integer, primary_key=True)
    parameter = Column(String, nullable=False)
    value = Column(String, nullable=False)
    unit = Column(String, nullable=False)
    source = Column(String, nullable=False)
    valid_time = Column(DateTime, nullable=False)
    retrieved_time = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"Observation(parameter={self.parameter}, value={self.value}, source={self.source}, retrieved_time={self.retrieved_time})"