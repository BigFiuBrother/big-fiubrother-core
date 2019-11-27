from sqlalchemy import Column, Integer, ForeignKey
from . import Base


class ProcessedVideoChunk(Base):
    __tablename__ = 'processed_video_chunks'

    frame_id = Column(Integer,
                      primary_key=True,
                      autoincrement=False,
                      ForeignKey('video_chunks.id', deferrable=True))
    total_frames_count = Column(Integer)
    processed_frames_count = Column(Integer)
