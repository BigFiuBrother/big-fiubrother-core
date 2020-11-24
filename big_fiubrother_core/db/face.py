from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from . import Base


class Face(Base):
    __tablename__ = 'face'

    id = Column(Integer, primary_key=True)
    frame_id = Column(Integer,
                      ForeignKey('frame.id', deferrable=True),
                      nullable=False)
    bounding_box = Column(JSONB, nullable=False)
    classification_id = Column(Integer,
                               ForeignKey('person.id', deferrable=True))
    probability_classification = Column(Float)
    is_match = Column(Boolean)
    person = relationship("Person", backref='Person', uselist=False)
