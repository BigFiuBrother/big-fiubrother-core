from sqlalchemy import Column, Integer, Float, String, Boolean
from sqlalchemy.orm import relationship
from big_fiubrother_core.db import Base


class VideoChunk(Base):
    __tablename__ = 'video_chunks'

    id = Column(Integer, primary_key=True)
    camera_id = Column(String, nullable=False)
    timestamp = Column(Float, nullable=False)
    processed = Column(Boolean, default=True, nullable=False)
    frames = relationship("Frame", order_by=lambda frame: frame.offset)

    def filename(self):
        return '{}_{}'.format(self.camera_id, int(self.timestamp))
