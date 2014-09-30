"""
Module for managing database with symbols.
"""
from contextlib import contextmanager

from sqlalchemy import Column, String, ForeignKey, Integer, create_engine
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from pisak import res


_SYMBOLS_DB_PATH = res.get("symbols_database.db")

_ENGINE_URL = "sqlite:///" + _SYMBOLS_DB_PATH


_Base = declarative_base()


class Symbol(_Base):
    __tablename__ = "symbols"
    id = Column(Integer, primary_key=True)
    path = Column(String, unique=True, nullable=False)
    text = Column(String, nullable=True)
    categories = relationship("Category", secondary="symbol_category_link",
                          collection_class=set, backref=backref(
                           "categories", lazy='noload', passive_updates=False))


class Category(_Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    path = Column(String, nullable=True)
    symbols = relationship("Symbol", secondary="symbol_category_link",
                          collection_class=set, backref=backref(
                            "symbols", lazy='noload', passive_updates=False))


class SymbolCategoryLink(_Base):
    __tablename__ = "symbol_category_link"
    symbol_id = Column(Integer, ForeignKey("symbols.id"), primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id"),
                         primary_key=True)


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


def get_all_symbols():
    """
    Return all symbols from the database.
    """
    with _establish_session() as sess:
        symbols = sess.query(Symbol).all()
        sess.expunge_all()
    return symbols


def get_all_categories():
    """
    Return all categories from the database.
    """
    with _establish_session() as sess:
        categories = sess.query(Category).all()
        sess.expunge_all()
    return categories


def get_all_symbols_from_category(category_id):
    """
    Return all symbols that belong to a category with the given id.
    :param category_id: id of a category
    """
    with _establish_session() as sess:
        symbols = sess.query(Symbol).filter(Symbol.categories.any(
            Category.id == category_id)).all()
        sess.expunge_all()
    return symbols


def insert_category(path=None, name):
    """
    Insert single record to the categories table in a database.
    :param name: name of the category 
    """
    with _establish_session() as sess:
        if not sess.query(Category).filter(Category.name == name).first():
            sess.add(Category(path=path, name=name))


def insert_symbol(path, text=None):
    """
    Insert single record to the symbols table in a database.
    :param path: path to the symbol file in the file system
    :param text: text related to the given symbol
    """
    with _establish_session() as sess:
        if not sess.query(Symbol).filter(Symbol.path == path).first():
            sess.add(Symbol(path=path, text=text))


def add_symbol_to_category(symbol_id, category_id):
    """
    Link a symbol with the given id with a category with the given id.
    :param symbol_id: id of the symbol
    :param category_id: id of the category
    """
    with _establish_session() as sess:
        symbol = sess.query(Symbol).filter(Symbol.id == symbol_id).first()
        category = sess.query(Category).filter(
            Category.id == category_id).first()
        if symbol and category:
            category.symbols.add(symbol)
