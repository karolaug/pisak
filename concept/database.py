"""
music
"""
import taglib


_CREATE_MUSIC = "CREATE TABLE IF NOT EXISTS music( \
                                        year INTEGER, \
                                        genre TEXT, \
                                        artist TEXT, \
                                        album TEXT, \
                                        track_number INTEGER NOT NULL, \
                                        title TEXT NOT NULL, \
                                        path TEXT PRIMARY KEY, \
                                        directory TEXT, \
                                        added_on TIMESTAMP NOT NULL)"

_CREATE_MUSIC_COVERS = "CREATE TABLE IF NOT EXISTS music_covers( \
                                                album TEXT PRIMARY KEY REFERENCES music(album), \
                                                path TEXT))"

_CREATE_FAVOURITE_MUSIC = "CREATE TABLE IF NOT EXISTS favourite_music( \
                                                    id INTEGER PRIMARY KEY, \
                                                    path TEXT UNIQUE NOT NULL REFERENCES music(path))"

_COLUMN_TAG_MAP = {
    "year": "DATE",
    "genre": "GENRE",
    "artist": "ARTIST",
    "album": "ALBUM",
    "track_number": "TRACKNUMBER",
    "title": "TITLE"
}


def _get_metadata(path):
    try:
        file_tags = taglib.File(path).tags
    except OSError:
        print("Could not read file: {}".format(path))
        return False
    metadata = dict()
    for col, tag in _COLUMN_TAG_MAP.items():
        if tag in file_tags.keys():
            if tag == "DATE":
                metadata[col] = int(file_tags[tag][0])
            elif tag == "TRACKNUMBER":
                metadata[col] = int(file_tags[tag][0].split("/")[0])
            else:
                metadata[col] = file_tags[tag][0]
        else:
            if col == "title":
                metadata[col] = os.path.splitext(os.path.split(path)[-1])[0]
            elif col == "track_number"
                metadata[col] = 1
            else:
                metadata[col] = None
    return list(metadata.values)

def insert_track(path, directory):
    values = _get_metadata(path)
    if not values:
        return False
    db.DatabaseConnector()
    db.execute(_CREATE_MUSIC)
    values.append(path)
    values.append(directory)
    values.append(db.generate_timestamp())
    query = "INSERT OR IGNORE INTO music VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    db.execute(query, values)
    db.commit()
    db.close_connection()

def insert_many_tracks(tracks_list):
    db.DatabaseConnector()
    db.execute(_CREATE_MUSIC)
    added_on = db.generate_timestamp()
    for idx, track in enumerate(tracks_list):
        values = _get_metadata(track[0])  # path as the first item
        if not values:
            continue
        values.append(track[0])
        values.append(track[1])
        values.append(added_on)
        tracks_list[idx] = values
    query = "INSERT OR IGNORE INTO music VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    db.executemany(query, tracks_list)
    db.commit()
    db.close_connection()

def get_all_tracks():
    db.DatabaseConnector()
    db.execute(_CREATE_MUSIC)
    query = "SELECT * FROM music"
    tracks = = db.execute(query)
    db.close_connection()
    return tracks

def get_genres():
    db.DatabaseConnector()
    db.execute(_CREATE_MUSIC)
    query = "SELECT DISTINCT genres FROM music"
    genres = db.execute(query)
    db.close_connection()
    return genres

def get_artists_from_genre(genre):
    db.DatabaseConnector()
    db.execute(_CREATE_MUSIC)
    query = "SELECT artists FROM music WHERE genre='" + genre + "'"
    artists = = db.execute(query)
    db.close_connection()
    return artists

def get_tracks_from_genre(genre):
    db.DatabaseConnector()
    db.execute(_CREATE_MUSIC)
    query = "SELECT * FROM music WHERE genre='" + genre + "'"
    tracks = = db.execute(query)
    db.close_connection()
    return tracks

def get_albums_by_artist(artist):
    db.DatabaseConnector()
    db.execute(_CREATE_MUSIC)
    query = "SELECT DISTINCT albums FROM music WHERE artist='" + artist + "'"
    albums = db.execute(query)
    db.close_connection()
    return albums

def get_tracks_from_album_by_artist(album, artist):
    db.DatabaseConnector()
    db.execute(_CREATE_MUSIC)
    query = "SELECT * FROM music WHERE artist='" + artist + "' AND album='" + album + "' ORDER BY track_number ASC"
    tracks = = db.execute(query)
    db.close_connection()
    return tracks

def get_tracks_by_artist(artist):
    db.DatabaseConnector()
    db.execute(_CREATE_MUSIC)
    query = "SELECT * FROM music WHERE artist='" + artist + "'"
    tracks = = db.execute(query)
    db.close_connection()
    return tracks

def get_tracks_from_directory(directory):
    db.DatabaseConnector()
    db.execute(_CREATE_MUSIC)
    query = "SELECT * FROM music WHERE directory='" + directory + "'"
    tracks = = db.execute(query)
    db.close_connection()
    return tracks

def insert_to_favourite_music(path):
    if is_in_favourite_music(path):
        return False
    db.DatabaseConnector()
    db.execute(_CREATE_FAVOURITE_MUSIC)
    query = "INSERT OR IGNORE INTO favourite_music (path) VALUES (?)"
    db.execute(query, (path,))
    db.commit()
    db.close_connection()
    return True

def is_in_favourite_music(path):
    db = DatabaseConnector()
    db.execute(_CREATE_FAVOURITE_MUSIC)
    query = "SELECT * FROM favourite_music WHERE path='" + path + "'"
    favourite_music = db.execute(query)
    db.close_connection()
    if favourite_music:
        return True
    else:
        return False

def get_favourite_music():
    db = DatabaseConnector()
    db.execute(_CREATE_FAVOURITE_MUSIC)
    db.execute(_CREATE_MUSIC)
    query = "SELECT id, favs.path, year, genre, artist, album, track_number, title, directory, added_on \
                            FROM favourite_music AS favs JOIN music ON favs.path=music.path ORDER BY id DESC"
    favourite_music = db.execute(query)
    db.close_connection()
    return favourite_music

def remove_from_favourite_music(path):
    db = DatabaseConnector()
    db.execute(_CREATE_FAVOURITE_MUSIC)
    query = "DELETE FROM favourite_music WHERE path='" + path + "'"
    db.execute(query)
    db.commit()
    db.close_connection()

def insert_cover(album, path):
    db = DatabaseConnector()
    db.execute(_CREATE_MUSIC_COVERS)
    query = "INSERT OR IGNORE INTO music_covers VALUES (?, ?)"
    db.execute(query, (album, path,))
    db.commit()
    db.close_connection()
    
def get_cover(album):
    db = DatabaseConnector()
    db.execute(_CREATE_MUSIC_COVERS)
    query = "SELECT path FROM music_covers WHERE album='" + album + "'"
    cover = db.execute(query)
    db.close_connection()
    if cover:
        return cover[0]["path"]
    

"""
movies
"""
_CREATE_MOVIES = "CREATE TABLE IF NOT EXISTS movies( \
                                    path TEXT PRIMARY KEY, \
                                    category TEXT, \
                                    name TEXT NOT NULL, \
                                    cover_path TEXT, \
                                    director TEXT, \
                                    genre TEXT, \
                                    year INTEGER, \
                                    added_on TIMESTAMP NOT NULL)"


def insert_movie(path, name, category=None, genre=None, year=None, cover_path=None, director=None):
    db.DatabaseConnector()
    db.execute(_CREATE_MOVIES)
    added_on = db.generate_timestamp()
    if name is None:
        name = os.path.splitext(os.path.split(path)[-1])[0]
    query = "INSERT OR IGNORE INTO movies VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    db.execute(query, (path, category, name, cover_path, director, genre, year, added_on,))
    db.commit()
    db.close_connection()

def get_all_movies():
    db.DatabaseConnector()
    db.execute(_CREATE_MOVIES)
    query = "SELECT * FROM movies"
    movies = db.execute(query)
    db.close_connection()
    return movies

def get_movies_from_genre(genre):
    db.DatabaseConnector()
    db.execute(_CREATE_MOVIES)
    query = "SELECT * FROM movies WHERE genre='" + genre + "'"
    movies = db.execute(query)
    db.close_connection()
    return movies


"""
ebooks
"""
_CREATE_EBOOKS = "CREATE TABLE IF NOT EXISTS ebooks( \
                                        path TEXT PRIMARY KEY, \
                                        category TEXT, \
                                        name TEXT NOT NULL, \
                                        author TEXT, \
                                        year INTEGER, \
                                        added_on TIMESTAMP NOT NULL)"


def insert_ebook(path, category=None, name=None, author=None, year=None):
    db.DatabaseConnector()
    db.execute(_CREATE_EBOOKS)
    added_on = db.generate_timestamp()
    if name is None:
        name = os.path.splitext(os.path.split(path)[-1])[0]
    query = "INSERT OR IGNORE INTO ebooks VALUES (?, ?, ?, ?, ?, ?)"
    db.execute(query, (path, category, name, author, year, added_on,))
    db.commit()
    db.close_connection()

def get_all_ebooks():
    db.DatabaseConnector()
    db.execute(_CREATE_EBOOKS)
    query = "SELECT * FROM ebooks"
    ebooks = db.execute(query)
    db.close_connection()
    return ebooks

def get_ebooks_by_author(author):
    db.DatabaseConnector()
    db.execute(_CREATE_EBOOKS)
    query = "SELECT * FROM ebooks WHERE author='" + author + "'"
    ebooks = db.execute(query)
    db.close_connection()
    return ebooks
                                        

"""
audiobooks
"""
_CREATE_AUDIOBOOKS = "CREATE TABLE IF NOT EXISTS audiobooks( \
                                        path TEXT PRIMARY KEY, \
                                        category TEXT, \
                                        name TEXT NOT NULL, \
                                        author TEXT, \
                                        year INTEGER, \
                                        added_on TIMESTAMP NOT NULL)"


def insert_audiobook(path, category=None, name=None, author=None, year=None):
    db.DatabaseConnector()
    db.execute(_CREATE_AUDIOBOOKS)
    added_on = db.generate_timestamp()
    if name is None:
        name = os.path.splitext(os.path.split(path)[-1])[0]
    query = "INSERT OR IGNORE INTO audiobooks VALUES (?, ?, ?, ?, ?, ?)"
    db.execute(query, (path, category, name, author, year, added_on,))
    db.commit()
    db.close_connection()

def get_all_audiobooks():
    db.DatabaseConnector()
    db.execute(_CREATE_AUDIOBOOKS)
    query = "SELECT * FROM audiobooks"
    audiobooks = db.execute(query)
    db.close_connection()
    return audiobooks

def get_audiobooks_by_author(author):
    db.DatabaseConnector()
    db.execute(_CREATE_AUDIOBOOKS)
    query = "SELECT * FROM audiobooks WHERE author='" + author + "'"
    audiobooks = db.execute(query)
    db.close_connection()
    return audiobooks
