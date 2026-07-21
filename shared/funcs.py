import hashlib
import shutil
from mathutils import Vector
import string
import uuid
import random
import time
from pathlib import Path
import tempfile

def subtract_from_vector(v: Vector, f: float) -> Vector:
    """Subtract a float value from each component of a vector."""
    r: Vector = Vector((0, 0, 0))
    r.x = v.x - f
    r.y = v.y - f
    r.z = v.z - f
    return r


def add_to_vector(v: Vector, f: float) -> Vector:
    """Add a float value to each component of a vector."""
    r: Vector = Vector((0, 0, 0))
    r.x = v.x + f
    r.y = v.y + f
    r.z = v.z + f
    return r


def get_min_vector_list(vecs: list) -> Vector:
    """Get the minimum vector from a list of vectors."""
    x: list = []
    y: list = []
    z: list = []
    for v in vecs:
        x.append(v[0])
        y.append(v[1])
        z.append(v[2])
    return Vector((min(x), min(y), min(z)))


def get_max_vector_list(vecs: list) -> Vector:
    """Return the maximum vector from a list of vectors."""
    x: list = []
    y: list = []
    z: list = []
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

def try_parse_int(value: str) -> int | None:
    """Try to parse a string as an integer."""
    try:
        return int(value)
    except ValueError:
        return None


def delete_folder(path: str) -> None:
    """Delete a folder and all its contents."""
    shutil.rmtree(path)


def poll_all(context, *predicates) -> bool:
    """Return True if all predicates return True for the given context."""
    return all(p(context) for p in predicates)


def get_folder_list_from_dir(dir: str) -> list[str]:
    """Get a list of all folders in a directory."""
    return [str(p) for p in Path(dir).rglob("*") if p.is_dir()]


def get_files_by_ext(path: str, ext: str) -> list[str]:
    """Get a list of all files with a specific extension in a directory."""
    return [str(p) for p in Path(path).rglob(f"*.{ext}")]

def generate_power_of_two_enum(max_power) -> list[tuple[str, str, str]]:
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

def enum_to_mask(enum_set) -> int:
    """Convert a set of enum identifiers to a bitmask."""
    return sum(int(x) for x in enum_set)

def mask_to_enum(mask, enum_items) -> set:
    """Convert a bitmask to a set of enum identifiers."""
    out = set()
    for ident, *_ in enum_items:
        bit = int(ident)
        if mask & bit:
            out.add(ident)
    return out

def enum_items_to_valid_mask(enum_items) -> int:
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

def indices_to_faces(indices) -> list[tuple]:
    """Convert a list of indices to a list of faces (triplets)."""
    return [(indices[i], indices[i+1], indices[i+2])
            for i in range(0, len(indices), 3)]

def create_temp_folder():
    return tempfile.mkdtemp()