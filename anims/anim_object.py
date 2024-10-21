from dataclasses import dataclass
from bpy.types import Object
from typing import List
from .target import Target

@dataclass
class AnimObject:
    """A class to store information about an animated object"""
    obj: Object
    flags: int
    sollum_type: str
    uv_anims: bool = False
    skel_anims: bool = False
    targets: List[Target] = None
    is_ped: bool = False