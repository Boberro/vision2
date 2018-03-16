# -*- coding: utf-8 -*-
from .meta import Base
from sqlalchemy import Column, VARCHAR, BOOLEAN
from sqlalchemy.sql.expression import false


class UploadedImage(Base):
    __tablename__ = 'uploaded_image'

    uid = Column(VARCHAR(64), nullable=False)
    filename = Column(VARCHAR(256), nullable=False)
