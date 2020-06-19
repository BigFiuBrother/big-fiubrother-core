from sqlalchemy import Column, Integer, Float, String
from big_fiubrother_core.db import Base


class VideoChunk(Base):
    __tablename__ = 'video_chunks'

    id = Column(Integer, primary_key=True)
    camera_id = Column(String, nullable=False)
    timestamp = Column(Float, nullable=False)

    def filename(self):
        return '{}_{}'.format(self.camera_id, int(self.timestamp))
