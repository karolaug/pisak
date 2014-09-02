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

def get_dir(folder):
    '''Returns path to XDG folder
    :param: folder - folder name as str, lowercase, possible are:
    desktop, documents, downloads, music, pictures, public, templates, videos
    '''
    return GLib.get_user_special_dir(FOLDERS[folder])

if __name__ == '__main__':
    print("Your XDG paths are:")
    for i in FOLDERS:
        print(get_dir(i))
