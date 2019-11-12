from sqlalchemy import Column, Integer, LargeBinary, ForeignKey
from big_fiubrother_core.db import Base


class AnalyzedVideoChunk(Base):
    __tablename__ = 'analyzed_video_chunks'

    id = Column(Integer, primary_key=True)
    video_chunk_id = Column(Integer, ForeignKey('video_chunks.id'), nullable=False, unique=True)
    payload = Column(LargeBinary)
