import bpy
from typing import NamedTuple
from pathlib import Path

class ImageInfo(NamedTuple):
    image: bpy.types.Image
    material: str
    flag_tint: bool = False
    flag_0: bool = False
    flag_1: bool = False
    
    @property
    def image_name(self) -> str:
        return Path(self.image.filepath).stem if self.image.filepath else ''
    
    @property
    def image_format(self) -> str:
        return Path(self.image.filepath).suffix if self.image.filepath else ''
    
    @property
    def image_path(self) -> str:
        return bpy.path.abspath(self.image.filepath) if self.image.filepath else ''