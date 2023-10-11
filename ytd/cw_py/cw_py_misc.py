import os


def jenkhash(key: str) -> int:
    hash_ = 0
    for char in key:
        hash_ += ord(char)
        hash_ += (hash_ << 10)
        hash_ ^= (hash_ >> 6)
    hash_ += (hash_ << 3)
    hash_ ^= (hash_ >> 11)
    hash_ += (hash_ << 15)
    return hash_ & 0xFFFFFFFF


def get_folder_list_from_dir(dir: str):
    folders = []
    for dirpath, dirnames, filenames in os.walk(dir):
        for dirname in dirnames:
            folders.append(os.path.join(dirpath, dirname))
    return folders
