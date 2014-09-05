"""
Module for managing photos specific database.
"""
import os
from contextlib import contextmanager

from sqlalchemy import Column, DateTime, String, ForeignKey, Integer, Boolean, \
     func, create_engine, desc, insert, select, update
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import UniqueConstraint

from pisak import res


_PHOTOS_DB_PATH = os.path.join(res.PATH, "photos_database.db")

_ENGINE_URL = "sqlite:///" + _PHOTOS_DB_PATH


Base = declarative_base()


class Photo(Base):
    __tablename__ = "photos"
    id = Column(Integer, primary_key=True)
    path = Column(String, unique=True, nullable=False)
    albums = relationship("Album", secondary="photo_album_link", collection_class=set,
                        backref=backref("albums", lazy='noload', passive_updates=False))
    created_on = Column(DateTime, nullable=False)
    is_favourite = Column(Boolean, nullable=False, default=False)
    added_on = Column(DateTime, nullable=False, default=func.now())
    

class Album(Base):
    __tablename__ = "albums"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    photos = relationship("Photo", secondary="photo_album_link", collection_class=set,
                        backref=backref("photos", lazy='noload', passive_updates=False))
    added_on = Column(DateTime, nullable=False, default=func.now())


class PhotoAlbumLink(Base):
    __tablename__ = "photo_album_link"
    photo_id = Column(Integer, ForeignKey("photos.id"), primary_key=True)
    album_id = Column(Integer, ForeignKey("albums.id"), primary_key=True)

    
@contextmanager
def _establish_session():
    engine = create_engine(_ENGINE_URL)
    Base.metadata.create_all(engine)
    session = sessionmaker(autoflush=False)
    session.configure(bind=engine)
    db_session = session()
    try:
        yield db_session
        db_session.commit()
    except:
        db_session.rollback()
        raise
    finally:
        db_session.close()


def is_db_empty():
    with _establish_session() as sess:
        item = sess.query(Album).first()
    if item:
        return False
    else:
        return True


def get_db_last_modification_time():
    return os.path.getmtime(_PHOTOS_DB_PATH)


def get_last_photo_insertion_time():
    with _establish_session() as sess:
        item = sess.execute(select([Photo.added_on]).order_by(
            desc(Photo.added_on))).fetchone()
    if item:
        return item.added_on
    else:
        return None


def get_last_album_insertion_time():
    with _establish_session() as sess:
        item = sess.execute(select([Album.added_on]).order_by(
            desc(Album.added_on))).fetchone()
    if item:
        return item.added_on
    else:
        return None
                            

def get_all_albums():
    with _establish_session() as sess:
        albums = sess.execute(select([Album])).fetchall()
    return albums


def get_album_with_id(album_id):
    with _establish_session() as sess:
        album = sess.execute(select([Album]).where(Album.id==album_id)).fetchone()
    return album


def get_photos_from_album(album_name):
    with _establish_session() as sess:
        photos = sess.query(Photo).filter(Photo.albums.any(Album.name==album_name)).order_by(
            Photo.created_on, desc(Photo.added_on)).all()
        sess.expunge_all()
    return photos


def get_photos_from_album_with_id(album_id):
    with _establish_session() as sess:
        photos = sess.query(Photo).filter(Photo.albums.any(
            Album.id==album_id)).order_by(Photo.created_on, desc(Photo.added_on)).all()
        sess.expunge_all()
    return photos


def get_all_photos():
    with _establish_session() as sess:
        photos = sess.execute(select([Photo]).order_by(
            Photo.created_on, desc(Photo.added_on))).fetchall()
    return photos


def get_photo_with_id(photo_id):
    with _establish_session() as sess:
        photo = sess.execute(select([Photo]).where(Photo.id==photo_id)).fetchone()
    return photo


def get_preview_of_album(album_name):
    with _establish_session() as sess:
        preview = sess.query(Photo).filter(Photo.albums.any(
            Album.name==album_name)).first()
        sess.expunge_all()
    return preview


def get_preview_of_album_with_id(album_id):
    with _establish_session() as sess:
        preview = sess.query(Photo).filter(Photo.albums.any(
            Album.id==album_id)).first()
        sess.expunge_all()
    return preview


def add_to_favourite_photos(photo_id):
    with _establish_session() as sess:
        sess.execute(update(Photo.__table__).where(Photo.id==photo_id).values(is_favourite=True))


def remove_from_favourite_photos(photo_id):
    with _establish_session() as sess:
        sess.execute(update(Photo.__table__).where(Photo.id==photo_id).values(is_favourite=False))
        

def get_favourite_photos():
    with _establish_session() as sess:
        photos = sess.query(Photo).filter(Photo.is_favourite==True).all()
        sess.expunge_all()
    return photos


def insert_album(album_name):
    with _establish_session() as sess:
        sess.execute(insert(Album.__table__, values={"name": album_name}).prefix_with("OR IGNORE"))


def insert_many_albums(albums_list):
    albums_list = [{"name": album} for album in albums_list]
    with _establish_session() as sess:
        sess.execute(insert(Album.__table__, values=albums_list).prefix_with("OR IGNORE"))
        

def insert_many_photos(photos_list):
    with _establish_session() as sess:
        for idx, photo in enumerate(photos_list):
            album = sess.query(Album).filter(Album.name==photo[2]).first()
            new_photo = Photo(path=photo[0], created_on=photo[1])
            album.photos.add(new_photo)
            sess.add(new_photo)


def insert_many_photos_to_album(photos_list, album_name):
    with _establish_session() as sess:
        album = sess.query(Album).filter(Album.name==album_name).first()
        for idx, photo in enumerate(photos_list):
            new_photo = Photo(path=photo[0], created_on=photo[1])
            album.photos.add(new_photo)
            sess.add(new_photo)
