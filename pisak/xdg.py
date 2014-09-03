'''
Module to govern the xdg directories.
'''
from gi.repository import GLib

FOLDERS = {"desktop" : GLib.USER_DIRECTORY_DESKTOP,
           "documents" : GLib.USER_DIRECTORY_DOCUMENTS,
           "downloads" : GLib.USER_DIRECTORY_DOWNLOAD,
           "music" : GLib.USER_DIRECTORY_MUSIC,
           "pictures" : GLib.USER_DIRECTORY_PICTURES,
           "public" : GLib.USER_DIRECTORY_PUBLIC_SHARE,
           "templates" : GLib.USER_DIRECTORY_TEMPLATES,
           "videos" : GLib.USER_DIRECTORY_VIDEOS}

def get_dir(which):
    return GLib.get_user_special_dir(FOLDERS[which])

if __name__ == '__main__':
    print("Your XDG paths are:")
    for i in FOLDERS:
        print(get_dir(i))
