from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from . import Base


class Face(Base):
    __tablename__ = 'faces'

    id = Column(Integer, primary_key=True)
    frame_id = Column(Integer, ForeignKey('frames.id'), nullable=False)
    bounding_box = Column(JSONB)
    classification_id = Column(Integer, ForeignKey('people.id'))
    probability_id = Column(Float)