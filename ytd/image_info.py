from typing import NamedTuple
from pathlib import Path

class ImageInfo(NamedTuple):
    """A class to store information about an image"""
    img_path: str
    material: str
    flag_tint: bool = False
    flag_0: bool = False
    flag_1: bool = False
 
    @property
    def img_name_full(self) -> str:
        """Returns image's full name including its extension"""
        return Path(self.img_path).name if self.img_path else ''

    @property
    def img_ext(self) -> str:
        """Returns image's extension"""
        return Path(self.img_path).suffix if self.img_path else ''
    
    @property
    def img_name(self) -> str:
        """Returns image's name without its extension"""
        return Path(self.img_path).stem if self.img_path else ''