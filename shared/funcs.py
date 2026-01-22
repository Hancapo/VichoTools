import hashlib
import shutil
from mathutils import Vector
import string
import uuid
import random
import time
import math
from pathlib import Path


def subtract_from_vector(v, f) -> Vector:
    """Subtract a float value from each component of a vector."""
    r = Vector((0, 0, 0))
    r.x = v.x - f
    r.y = v.y - f
    r.z = v.z - f
    return r


def add_to_vector(v, f) -> Vector:
    """Add a float value to each component of a vector."""
    r = Vector((0, 0, 0))
    r.x = v.x + f
    r.y = v.y + f
    r.z = v.z + f
    return r


def get_min_vector_list(vecs) -> Vector:
    """Get the minimum vector from a list of vectors."""
    x = []
    y = []
    z = []
    for v in vecs:
        x.append(v[0])
        y.append(v[1])
        z.append(v[2])
    return Vector((min(x), min(y), min(z)))


def get_max_vector_list(vecs) -> Vector:
    """Return the maximum vector from a list of vectors."""
    x = []
    y = []
    z = []
    for v in vecs:
        x.append(v[0])
        y.append(v[1])
        z.append(v[2])
    return Vector((max(x), max(y), max(z)))


def get_random_string(length=8):
    """Generate a random string of specified length."""
    chars = string.ascii_letters + string.digits
    rd_part = "".join(random.choice(chars) for _ in range(length))
    ts = str(int(time.time()))[-4:]
    uuid_str = str(uuid.uuid4()).replace("-", "")[:4]
    rdm_str = f"{rd_part}{ts}{uuid_str}"
    return rdm_str


def get_jenkins_hash(name: str) -> int:
    """Compute the Jenkins hash for a given string."""
    hash = 0
    for char in name:
        hash += ord(char)
        hash += hash << 10
        hash ^= hash >> 6
    hash += hash << 3
    hash ^= hash >> 11
    hash += hash << 15
    return hash & 0xFFFFFFFF


def try_parse_int(value: str) -> int | None:
    """Try to parse a string as an integer."""
    try:
        return int(value)
    except ValueError:
        return None


def delete_folder(path: str) -> None:
    """Delete a folder and all its contents."""
    shutil.rmtree(path)


def poll_all(context, *predicates):
    """Return True if all predicates return True for the given context."""
    return all(p(context) for p in predicates)


def get_folder_list_from_dir(dir: str):
    """Get a list of all folders in a directory."""
    return [str(p) for p in Path(dir).rglob("*") if p.is_dir()]


def get_files_by_ext(path: str, ext: str) -> list[str]:
    """Get a list of all files with a specific extension in a directory."""
    return [str(p) for p in Path(path).rglob(f"*.{ext}")]


def calculate_mipmaps_lvls(width: int, height: int) -> int:
    """Calculate the number of mipmap levels for given dimensions."""
    if width <= 4 or height <= 4:
        return 1
    levels = 1
    while width > 4 and height > 4:
        width = max(1, width // 2)
        height = max(1, height // 2)
        levels += 1
    return levels


def closest_pow2(value):
    """"Find the closest power of two to a given value."""
    lower_power = 1
    while lower_power * 2 <= value:
        lower_power *= 2
    higher_power = lower_power * 2
    return lower_power if (value - lower_power < higher_power - value) else higher_power


def closest_pow2_dims(
    width: int, height: int, max_dimension: int, make_half: bool
) -> tuple[int, int]:
    """Calculate the closest power of two dimensions with constraints."""
    width, height = closest_pow2(width), closest_pow2(height)
    new_width, new_height = width, height

    if max_dimension == 0:
        max_dimension = max(width, height)

    use_width = width % max_dimension == 0
    use_height = height % max_dimension == 0

    if use_width and use_height:
        if width / max_dimension > height / max_dimension:
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

def generate_power_of_two_enum(max_power):
    """Generate a list of power of two tuples up to a maximum power."""
    return [(str(2**i), str(2**i), str(2**i)) for i in range(2, max_power + 1)]

def sanitize_name(name: str) -> str:
    """Gets the name before any dots"""
    new_name: str = ""
    if '.' in name:
        new_name = name.split('.')[0]
    else:
        new_name = name
    return new_name

def set_bit(value: int, bit: int) -> int:
    """Sets a specific bit in an integer value"""
    return value | (1 << bit)

def enum_to_mask(enum_set):
    """Convert a set of enum identifiers to a bitmask."""
    return sum(int(x) for x in enum_set)

def mask_to_enum(mask, enum_items):
    """Convert a bitmask to a set of enum identifiers."""
    out = set()
    for ident, *_ in enum_items:
        bit = int(ident)
        if mask & bit:
            out.add(ident)
    return out

def enum_items_to_valid_mask(enum_items):
    """Get a valid bitmask from enum items."""
    return sum(int(ident) for ident, *_ in enum_items)

def get_fn_wt_ext(file_path: str) -> str:
    """Get the file name without extension from a file path."""
    return Path(file_path).stem

def get_hash_from_bytes(data: bytes, algorithm:str = "sha256") -> str:
    """Returns the hash of the data"""
    hash_object = hashlib.new(algorithm)
    hash_object.update(data)
    return hash_object.hexdigest()