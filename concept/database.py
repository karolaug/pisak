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
                                        path TEXT PRIMARY KEY NOT NULL, \
                                        directory TEXT, \
                                        added_on TIMESTAMP)"

_CREATE_FAVOURITE_MUSIC = "CREATE TABLE IF NOT EXISTS favourite_music( \
                                                    id INTEGER PRIMARY KEY, \
                                                    path TEXT UNIQUE NOT NULL REFERENCES path(music))"

_COLUMN_TAG_MAP = {
    "year": "DATE", "genre": "GENRE", "artist": "ARTIST",
    "album": "ALBUM", "track_number": "TRACKNUMBER", "title": "TITLE"
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
            metadata[col] = file_tags[tag][0]
        else:
            metadata[col] = None
    if not metadata["title"]:
        metadata["title"] = os.path.splitext(os.path.split(path)[-1])[0]
    return list(metadata.values)

def remove_from_favourite_music(path):
    db = DatabaseConnector()
    db.execute(_CREATE_FAVOURITE_MUSIC)
    query = "DELETE FROM favourite_music WHERE path='" + path + "'"
    db.execute(query)
    db.commit()
    db.close_connection()

def get_favourite_music():
    db = DatabaseConnector()
    db.execute(_CREATE_FAVOURITE_MUSIC)
    db.execute(_CREATE_MUSIC)
    query = "SELECT id, favs.path, year, genre, artist, album, track_number, title, directory, added_on \
                            FROM favourite_music AS favs JOIN music ON favs.path=music.path ORDER BY id DESC"
    favourite_music = db.execute(query)
    db.close_connection()
    return favourite_music

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
    return True

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
    return True

def get_tracks_from_directory(directory):
    db.DatabaseConnector()
    db.execute(_CREATE_MUSIC)
    query = "SELECT * FROM music WHERE directory='" + directory + "'"
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
