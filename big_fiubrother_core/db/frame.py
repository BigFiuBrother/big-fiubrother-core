from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from . import Base


class Frame(Base):
    __tablename__ = 'frames'

    id = Column(Integer, primary_key=True)
    offset = Column(Integer, nullable=False)
    video_chunk_id = Column(Integer,
                            ForeignKey('video_chunks.id', deferrable=True),
                            nullable=False)
    faces = relationship("Face", backref='Face')
