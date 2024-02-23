# coding: utf-8
from sqlalchemy import Column, Float, String, Table, Text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class LectureInfo(Base):
    __tablename__ = 'lecture_info'

    학기 = Column(INTEGER(11))
    학수번호 = Column(String(2))
    강의아이디 = Column(INTEGER(11), primary_key=True)
    교수명 = Column(String(255))
    강의요일 = Column(String(255))
    강의시간 = Column(INTEGER(11))
    강의만족도 = Column(Float)
    학습량 = Column(Float)
    난이도 = Column(Float)
    강의력 = Column(Float)
    성취감 = Column(Float)


t_lecture_repu = Table(
    'lecture_repu', metadata,
    Column('강의아이디', INTEGER(11)),
    Column('유저아이디', String(255)),
    Column('강의만족도', INTEGER(11)),
    Column('학습량', INTEGER(11)),
    Column('난이도', INTEGER(11)),
    Column('강의력', INTEGER(11)),
    Column('성취감', INTEGER(11)),
    Column('강의평', Text)
)
