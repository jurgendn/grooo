import os


def remove_old_files():
    path = './static/files/'
    files_list = os.listdir(path)
    for fname in files_list:
        print(fname)
        os.remove(path + fname)
    return True