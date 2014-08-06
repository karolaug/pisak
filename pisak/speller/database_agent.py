from pisak.database_manager import DatabaseConnector


APP_NAME = "speller"


def insert_text_file(name):
    db = DatabaseConnector()
    values = (db.generate_new_path(APP_NAME), name, db.generate_timestamp(),)
    db.add_record(APP_NAME, values)
    db.commit()
    db.close_connection()

def get_text_files():
    db = DatabaseConnector()
    text_files = db.get_all_records(APP_NAME)
    db.close_connection()
    return text_files

