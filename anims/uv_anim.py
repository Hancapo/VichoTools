from dataclasses import dataclass
from bpy.types import Material, Action

@dataclass
class UvAnim:
    material: Material
    action: Action
    material_idx: int