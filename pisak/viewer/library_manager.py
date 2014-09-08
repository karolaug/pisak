"""
Module with functions for searching and loading photos and folders
from the file system's default pictures directory.
"""
import os
from contextlib import contextmanager
# import imghdr  # another possibility

from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pisak import xdg, res


#: Path to the system's default pictures directory
LIBRARY_DIR = xdg.get_dir("pictures")


#: Extensions of the supported file formats
EXTENSIONS = (".png", ".jpg", ".jpeg", ".tiff", ".gif", ".raw", ".bmp")


#: Path to the database with favourite photos
FAVOURITE_PHOTOS_DB_PATH = os.path.join(res.PATH, "favourite_photos.db")


#: String constant for sqlalchemy internal purposes
_ENGINE_URL = "sqlite:///" + FAVOURITE_PHOTOS_DB_PATH


#: Declarative base class for sqlalchemy classes definitions
_Base = declarative_base()


def get_all_albums():
    """
    Return the list of folders from inside the default directory
    """
    return [item[0] for item in os.walk(LIBRARY_DIR)]


def get_photos_from_album(album):
    """
    Return the list of files in the given folder whose names fullfill
    the extensions' condition
    :param album: path to the folder
    """
    return [os.path.join(album, file) for file in os.listdir(album) if
            os.path.splitext(file)[-1].lower() in EXTENSIONS]


def get_preview_of_album(album):
    """
    Return the path to the first file in the given folder whose name fullfill
    the extensions' condition, or None
    :param album: path to the folder
    """
    for file in os.listdir(album):
        if os.path.splitext(file)[-1].lower() in EXTENSIONS:
            return os.path.join(album, file)

        
def add_to_favourite_photos(photo):
    """
    Mark the given photo as one of the favourites by adding
    it to the database.
    :param photo: path to the photo
    """
    if not is_in_favourite_photos(photo):
        with _establish_session() as sess:
            sess.add(FavouritePhoto(path=photo))


def is_in_favourite_photos(photo):
    """
    Check if a given photo is one of the favourites.
    :param photo: path to the photo
    """
    with _establish_session() as sess:
        fav = sess.query(FavouritePhoto).filter(
            FavouritePhoto.path == photo).first()
    if fav:
        return True
    else:
        return False
    

def remove_from_favourite_photos(photo):
    """
    Remove the given photo from favourites.
    :param photo: path to the photo
    """
    if is_in_favourite_photos(photo):
        with _establish_session() as sess:
            sess.query(FavouritePhoto).filter(
                FavouritePhoto.path == photo).delete()


def get_favourite_photos():
    """
    Return a list of all favourite photos. Check every one if
    still exists as a file in the file system and remove from favourites if not.
    """
    with _establish_session() as sess:
        favs = sess.query(FavouritePhoto).all()
        sess.expunge_all()
    for item in favs:
        if not os.path.exists(item.path):
            remove_from_favourite_photos(item.path)
            favs.remove(item)
    return favs


@contextmanager
def _establish_session():
    engine = create_engine(_ENGINE_URL)
    _Base.metadata.create_all(engine)
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

        
class FavouritePhoto(_Base):
    """
    Class representing a row in the favourite photos table in a database
    """
    __tablename__ = "favourite_photos"
    id = Column(Integer, primary_key=True)
    path = Column(String, unique=True)
