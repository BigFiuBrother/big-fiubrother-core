from sqlalchemy import Column, Integer, Float, String, LargeBinary
from big_fiubrother_core.db import Base


class VideoChunk(Base):
    __tablename__ = 'video_chunks'

    id = Column(Integer, primary_key=True)
    camera_id = Column(String)
    timestamp = Column(Float)
    payload = Column(LargeBinary)
