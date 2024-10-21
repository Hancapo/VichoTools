from dataclasses import dataclass
from bpy.types import Object, Material, Action, Camera
from .enums import AnimationType

@dataclass
class Target:
    """A class to store information about an animation target"""
    target_id_type: AnimationType
    target_id: Object | Material | Camera
    action: Action
    material_idx: int | None = None