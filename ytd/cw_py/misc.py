from pathlib import Path
import math

SUPPORTED_FORMATS = [".png", ".jpg", ".bmp", ".tiff", ".tif", ".jpeg", ".psd", ".gif", ".webp"]


def get_folder_list_from_dir(dir: str):
    return [str(p) for p in Path(dir).rglob("*") if p.is_dir()]


def get_non_dds(path: str) -> list[str]:
    return [str(p) for p in Path(path).rglob("*") if p.suffix in SUPPORTED_FORMATS]


def get_dds(path: str) -> list[str]:
    return [str(p) for p in Path(path).rglob("*.dds")]


def calculate_mipmaps_lvls(width: int, height: int) -> int:
    if width <= 4 or height <= 4:
        return 1
    levels = 1
    while width > 4 and height > 4:
        width = max(1, width // 2)
        height = max(1, height // 2)
        levels += 1
    return levels

def closest_pow2(value):
    lower_power = 1

    while lower_power * 2 <= value:
        lower_power *= 2

    higher_power = lower_power * 2

    return lower_power if (value - lower_power < higher_power - value) else higher_power


def closest_pow2_dims(width: int, height: int, max_dimension: int, make_half: bool) -> tuple[int, int]:
    width, height = closest_pow2(width), closest_pow2(height)
    new_width, new_height = width, height
    
    if max_dimension == 0:
        max_dimension = max(width, height)
    
    use_width = True if width % max_dimension == 0 else False
    use_height = True if height % max_dimension == 0 else False
    
    if(use_width and use_height):
        if( width / max_dimension < height / max_dimension):
            num = width
        else:
            num = height
    elif use_width and not use_height:
        num = width
    else:
        num = height
    
    log_calc = math.log2(num / max_dimension)
    
    for _ in range(0, int(log_calc)):
        if new_width <= 4 or new_height <= 4:
            break
        new_width /= 2
        new_height /= 2
        
    if make_half:
        if new_width / 2 >= 4 and new_height / 2 >= 4:
            new_width /= 2
            new_height /= 2
    
    return int(new_width), int(new_height)