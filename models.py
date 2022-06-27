from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MetData(Base):
    __tablename__ = "metdata"

    enums_type = ("forecast", "observation")
    enums_source = ("YR", "SMHI")

    id = Column(Integer, primary_key=True)
    upload_id = Column(String, nullable=False)
    parameter = Column(String, nullable=False)
    value = Column(String, nullable=False)
    unit = Column(String, nullable=False)
    valid_time = Column(DateTime, nullable=False)
    retrieved_time = Column(DateTime, nullable=False)
    variant = Column(Enum(*enums_type), nullable=False)
    source = Column(Enum(*enums_source), nullable=False)

    def __repr__(self):
        return f"MetData(parameter={self.parameter}, value={self.value}, variant={self.variant}, source={self.source}, retrieved_time={self.retrieved_time})"
