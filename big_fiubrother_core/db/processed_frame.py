from sqlalchemy import Column, Integer, ForeignKey
from . import Base


class ProcessedFrame(Base):
    __tablename__ = 'processed_frames'

    frame_id = Column(Integer,
                      primary_key=True,
                      autoincrement=False,
                      ForeignKey('frames.id', deferrable=True))
    total_faces_count = Column(Integer)
    processed_faces_count = Column(Integer)
