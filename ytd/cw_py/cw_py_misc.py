from pathlib import Path
import numpy as np


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
    if np_array.shape[-1] != 4:
        return False
    return np.any(np_array[..., 3] < 255)
