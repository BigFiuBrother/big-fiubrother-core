from sqlalchemy import Column, Integer, ForeignKey
from . import Base


class ProcessedFrame(Base):
    __tablename__ = 'processed_frames'

    frame_id = Column(Integer,
                      ForeignKey('frames.id', deferrable=True),
                      primary_key=True,
                      autoincrement=False
                      )
    total_faces_count = Column(Integer)
    processed_faces_count = Column(Integer)
