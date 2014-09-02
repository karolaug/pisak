import os
from datetime import datetime
from contextlib import contextmanager

from gi.repository import GExiv2, GObject
from sqlalchemy import Column, DateTime, String, Integer, func, create_engine, desc, insert
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import UniqueConstraint

from pisak import res


_PHOTOS_DB_PATH = os.path.join(res.PATH, "photos_database.db")

_ENGINE_URL = "sqlite:///" + _PHOTOS_DB_PATH


Base = declarative_base()


class Photo(Base):
    __tablename__ = "photos"
    __table_args__ = (
        UniqueConstraint("path", "album"),
    )
    id = Column(Integer, primary_key=True)
    path = Column(String, nullable=False)
    album = Column(String, nullable=False)
    created_on = Column(DateTime, nullable=False)
    added_on = Column(DateTime, nullable=False, default=func.now())
    rating = Column(Integer)

    
@contextmanager
def _establish_session():
    engine = create_engine(_ENGINE_URL)
    Base.metadata.create_all(engine)
    session = sessionmaker()
    session.configure(bind=engine)
    db_session = session()
    try:
        yield db_session
        db_session.expunge_all()
        db_session.commit()
    except:
        db_session.rollback()
        raise
    finally:
        db_session.close()


def get_albums():
    with _establish_session() as sess:
        albums = sess.query(Photo.album).distinct().all()
    return albums


def get_photos_from_album(album):
    with _establish_session() as sess:
        photos = sess.query(Photo).filter(Photo.album==album).order_by(
            Photo.created_on, desc(Photo.added_on)).all()
    return photos


def get_all_photos():
    with _establish_session() as sess:
        photos = sess.query(Photo).order_by(
            Photo.created_on, desc(Photo.added_on)).all()
    return photos


def get_preview_of_album(album):
    with _establish_session() as sess:
        preview = sess.query(Photo).filter(Photo.album==album).one()
    return preview


def insert_photo(path, album):
    try:
        meta = GExiv2.Metadata(path)
        if meta.has_tag("Exif.Photo.DateTimeOriginal"):
            created_on = meta.get_date_time()
        else:
            created_on = datetime.fromtimestamp(os.path.getctime(path))
    except GObject.GError:
        created_on = datetime.fromtimestamp(os.path.getctime(path))
    photo = {"path": path, "album": album, "created_on": created_on}
    with _establish_session() as sess:
        sess.execute(insert(Photo.__table__, values=photo).prefix_with("OR IGNORE"))
    

def insert_many_photos(photos_list):
    for idx, photo in enumerate(photos_list):
        try:
            meta = GExiv2.Metadata(photo[0])  # photo path as the first item
            if meta.has_tag("Exif.Photo.DateTimeOriginal"):
                photo.append(meta.get_date_time())
            else:
                photo.append(datetime.fromtimestamp(os.path.getctime(photo[0])))
        except GObject.GErrordistinct:
            photo.append(datetime.fromtimestamp(os.path.getctime(photo[0])))
        photos_list[idx] = {"path": photo[0], "album": photo[1], "created_on": photo[2]}
    with _establish_session() as sess:
        sess.execute(insert(Photo.__table__, values=photos_list).prefix_with("OR IGNORE"))
