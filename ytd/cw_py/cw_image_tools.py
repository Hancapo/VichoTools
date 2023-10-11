from pathlib import Path
import numpy as np
import os

def get_non_dds(path: str) -> list[str]:
    non_dds = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in [f for f in filenames if 
                         f.endswith(".png") or 
                         f.endswith(".jpg") or
                         f.endswith(".jpeg") or 
                         f.endswith(".tga") or 
                         f.endswith(".bmp") or 
                         f.endswith(".tga")]:
            non_dds.append(os.path.join(dirpath, filename))
    return non_dds

def get_dds(path: str) -> list[str]:
    dds = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in [f for f in filenames if f.endswith(".dds")]:
            dds.append(os.path.join(dirpath, filename))
    return dds

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