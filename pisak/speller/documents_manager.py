"""
Module for managing text documents created with speller application and
database dedicated to them.
"""
import os
from contextlib import contextmanager

from sqlalchemy import Column, DateTime, String, Integer, func, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from pisak import xdg, res


#: Path to system's default documents directory
DOCUMENTS_DIR = xdg.get_dir("documents")


#: Common base for text documents' files' names
FILE_NAME_BASE = "text_file_no_"


#: Extension of files' names
FILE_NAME_EXTENSION = ".txt"


#: Path to database related to text documents
DOCUMENTS_DB_PATH = os.path.join(res.PATH, "documents.db")


#: String constant for sqlalchemy internal purposes
_ENGINE_URL = "sqlite:///" + DOCUMENTS_DB_PATH


#: Declarative base class for sqlalchemy classes definitions
_Base = declarative_base()


def get_all_documents():
    """
    Return all records from the database which are pointing to the
    existing files in the files' system.
    """
    with _establish_session() as sess:
        documents = sess.query(Document).all()
        sess.expunge_all()
    for item in documents:
        if not os.path.exists(item.path):
            remove_document(item.path)
            documents.remove(item)
    return documents


def remove_document(path):
    """
    Remove record from the datatabse pointing to the not existing file.
    :param path: path column of the requested to delete record
    """
    with _establish_session() as sess:
        sess.query(Document).filter(Document.path == path).delete()


def add_document(name):
    """
    Insert new document related record to the database.
    Return path in the file system to the new document.
    :param name: name of the new document
    """
    path = _generate_new_path()
    with _establish_session() as sess:
        sess.add(Document(path=path, name=name))
    return path


def _generate_new_path():
    """
    Generate path for the new document file.
    """
    with _establish_session() as sess:
        file_no = sess.query(Document).count()
    file_name = FILE_NAME_BASE + str(file_no) + FILE_NAME_EXTENSION
    while os.path.exists(os.path.join(DOCUMENTS_DIR, file_name)):
        file_no += 1
        file_name = FILE_NAME_BASE + str(file_no) + FILE_NAME_EXTENSION
    return os.path.join(DOCUMENTS_DIR, file_name)


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


class Document(_Base):
    """
    Class representing a row in the documents table in the database
    """
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    path = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    added_on = Column(DateTime, nullable=False, default=func.now())
