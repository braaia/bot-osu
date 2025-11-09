from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.orm import declarative_base

engine = create_engine("sqlite:///maps.db")

Base =  declarative_base()
Base.metadata.create_all(engine)

class ARZero(Base):
    __tablename__ = "AR0"

    id = Column(Integer, primary_key=True)
    beatmap_id = Column(Integer)
    diff_id = Column(Integer, unique=True)
    artist = Column(String)
    title = Column(String)
    star_rating = Column(Float)
    ar = Column(Float)
    bpm = Column(Integer)
    length = Column(Integer)
    ranked = Column(Integer)
    url = Column(String)

class AROito(Base):
    __tablename__ = "<=AR8"

    id = Column(Integer, primary_key=True)
    beatmap_id = Column(Integer)
    diff_id = Column(Integer, unique=True)
    artist = Column(String)
    title = Column(String)
    star_rating = Column(Float)
    ar = Column(Float)
    bpm = Column(Integer)
    length = Column(Integer)
    ranked = Column(Integer)
    url = Column(String)

class ARDez(Base):
    __tablename__ = "<=AR10"

    id = Column(Integer, primary_key=True)
    beatmap_id = Column(Integer)
    diff_id = Column(Integer, unique=True)
    artist = Column(String)
    title = Column(String)
    star_rating = Column(Float)
    ar = Column(Float)
    bpm = Column(Integer)
    length = Column(Integer)
    ranked = Column(Integer)
    url = Column(String)

class RecommendedMaps(Base):
    __tablename__ = "RecommendedMaps"

    id = Column(Integer, primary_key=True)
    beatmap_id = Column(Integer)
    diff_id = Column(Integer, unique=True)
    artist = Column(String)
    title = Column(String)
    star_rating = Column(Float)
    ar = Column(Float)
    bpm = Column(Integer)
    length = Column(Integer)
    ranked = Column(Integer)
    url = Column(String)

class AllMaps(Base):
    __tablename__ = "AllMaps"

    id = Column(Integer, primary_key=True)
    beatmap_id = Column(Integer)
    diff_id = Column(Integer, unique=True)
    artist = Column(String)
    title = Column(String)
    star_rating = Column(Float)
    ar = Column(Float)
    bpm = Column(Integer)
    length = Column(Integer)
    ranked = Column(Integer)
    url = Column(String)

