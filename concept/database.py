"""
music
"""
import taglib


_CREATE_MUSIC = "CREATE TABLE IF NOT EXISTS music( \
                                        year INTEGER, \
                                        genre TEXT, \
                                        artist TEXT, \
                                        album TEXT, \
                                        track_number INTEGER, \
                                        title TEXT NOT NULL, \
                                        path TEXT NOT NULL, \
                                        category TEXT NOT NULL, \
                                        added_on TIMESTAMP, \
                                        PRIMARY KEYS (path, category))"

_COLUMN_TAG_MAP = {
    "year": "DATE", "genre": "GENRE", "artist": "ARTIST",
    "album": "ALBUM", "track_number": "TRACKNUMBER", "title": "TITLE"
    }


def get_metadata(path):
    try:
        file_tags = taglib.File(path).tags
    except OSError:
        print("Could not read file: {}".format(path))
        return False
    metadata = dict()
    for col in _COLUMN_TAG_MAP.keys():
        tag = _COLUMN_TAG_MAP[col]
        if tag in file_tags.keys():
            metadata[col] = file_tags[tag][0]
        else:
            metadata[col] = None
    if not metadata["title"]:
        metadata["title"] = os.path.splitext(os.path.split(path)[-1])[0]
    return list(metadata.values)
  
def add_track(path, category):
    values = get_metadata(path)
    if not values:
        return False
    db.DatabaseConnector()
    db.execute(_CREATE_MUSIC)
    values.append(path)
    values.append(category)
    values.append(db.generate_timestamp())
    query = "INSERT OR IGNORE INTO music VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    db.execute(query, values)
    db.commit()
    db.close_connection()
    return True

def get_genres():
    db.DatabaseConnector()
    db.execute(_CREATE_MUSIC)
    query = "SELECT DISTINCT genres FROM music"
    genres = db.execute(query)
    db.close_connection()
    return genres

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

def get_artists_from_genre(genre):
    db.DatabaseConnector()
    db.execute(_CREATE_MUSIC)
    query = "SELECT artists FROM music WHERE genre='" + genre + "'"
    artists = = db.execute(query)
    db.close_connection()
    return artists

def get_tracks_by_artist(artist):
    db.DatabaseConnector()
    db.execute(_CREATE_MUSIC)
    query = "SELECT * FROM music WHERE artist='" + artist + "'"
    tracks = = db.execute(query)
    db.close_connection()
    return tracks

def get_all_tracks():
    db.DatabaseConnector()
    db.execute(_CREATE_MUSIC)
    query = "SELECT * FROM music"
    tracks = = db.execute(query)
    db.close_connection()
    return tracks

def get_tracks_from_genre(genre):
    db.DatabaseConnector()
    db.execute(_CREATE_MUSIC)
    query = "SELECT * FROM music WHERE genre='" + genre + "'"
    tracks = = db.execute(query)
    db.close_connection()
    return tracks


"""
movies
"""
# ...
