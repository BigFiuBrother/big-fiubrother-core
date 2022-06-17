from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from . import Base


class FaceEmbedding(Base):
    __tablename__ = 'face_embeddings'

    id = Column(Integer, primary_key=True)
    face_id = Column(Integer,
                     ForeignKey('faces.id', deferrable=True),
                     nullable=False)
    embedding = Column(ARRAY(Float), nullable=False)
