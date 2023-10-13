from pathlib import Path
import numpy as np

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
    return [str(p) for p in Path(dir).rglob('*') if p.is_dir()]


def get_non_dds(path: str) -> list[str]:
    supported_formats = ['.png', '.jpg', '.jpeg', '.tga', '.bmp']
    return [str(p) for p in Path(path).rglob('*') if p.suffix in supported_formats]


def get_dds(path: str) -> list[str]:
    return [str(p) for p in Path(path).rglob('*.dds')]


def calculate_mipmaps(width: int, height: int) -> int:
    mipmaps = 0
    while width > 4 and height > 4:
        width = width // 2
        height = height // 2
        mipmaps += 1
    return mipmaps


def has_transparency(image):
    np_array = np.array(image)
    if np_array.shape[2] == 4:
        return np.any(np_array[..., 3] < 255)
    else:
        return False
