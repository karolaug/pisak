import os

from pisak.viewer import model, database_agent


if __name__ == "__main__":
    path = os.getenv("HOME")
    print("Wyszukiwanie w : " + path)
    model.LIBRARY_SUBDIR = ""
    lib = model.Library(path)
    lib.scan()
    categories = database_agent.get_categories()
    if len(categories) > 0:
        print("Kategorie: ", ", ".join([i["category"] for i in categories]))
        photos = database_agent.get_photos(categories[-1]["category"])
        print("Zdjęcia w kategorii " + categories[-1]["category"] + ": ")
        for photo in photos:
            print(", ".join([str(list(photo.keys())[idx]) + ": " + str(j) for idx, j in enumerate(photo)]))
        database_agent.add_to_favourite_photos(photos[0]["path"], photos[0]["category"])
        print("Ulubione: ")
        for fav in database_agent.get_favourite_photos():
            print(", ".join([str(list(fav.keys())[idx]) + ": " + str(j) for idx,j in enumerate(fav)]))
    else:
        print("No photos at or below " + path)
    
    
