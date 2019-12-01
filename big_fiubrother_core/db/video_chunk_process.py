from sqlalchemy import Column, Integer, ForeignKey
from . import Base


class VideoChunkProcess(Base):
    __tablename__ = 'video_chunk_processes'

    video_chunk_id = Column(Integer,
                            ForeignKey('video_chunks.id', deferrable=True),
                            primary_key=True,
                            autoincrement=False)

    total_frames_count = Column(Integer, nullable=False)
    processed_frames_count = Column(Integer, nullable=False, default=0)

    def is_completed(self):
        return self.processed_frames_count == self.total_frames_count
