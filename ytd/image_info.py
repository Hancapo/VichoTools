from typing import NamedTuple
from pathlib import Path

class ImageInfo(NamedTuple):
    img_path: str
    material: str
    flag_tint: bool = False
    flag_0: bool = False
    flag_1: bool = False
 
    @property
    def img_name_full(self) -> str:
        """Returns the full name of the image including the extension"""
        return Path(self.img_path).name if self.img_path else ''

    @property
    def img_ext(self) -> str:
        """Returns the extension of the image"""
        return Path(self.img_path).suffix if self.img_path else ''
    
    @property
    def img_name(self) -> str:
        """Returns the name of the image without the extension"""
        return Path(self.img_path).stem if self.img_path else ''