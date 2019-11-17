from sqlalchemy import Column, Integer, ForeignKey
from . import Base


class Frame(Base):
    __tablename__ = 'frames'

    id = Column(Integer, primary_key=True)
    offset = Column(Integer)
    video_chunk_id = Column(Integer,
                            ForeignKey('video_chunks.id', deferrable=True),
                            nullable=False)
