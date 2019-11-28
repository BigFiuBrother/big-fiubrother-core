from sqlalchemy import Column, Integer, ForeignKey
from . import Base


class ProcessedVideoChunk(Base):
    __tablename__ = 'processed_video_chunks'

    frame_id = Column(Integer,
                      ForeignKey('video_chunks.id', deferrable=True),
                      primary_key=True,
                      autoincrement=False
                      )
    total_frames_count = Column(Integer)
    processed_frames_count = Column(Integer)
