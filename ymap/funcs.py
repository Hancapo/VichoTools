from ..vicho_dependencies import dependencies_manager as dm
from pathlib import Path

def get_ymap_name(ymap) -> str:
    """Returns the name of the YMAP"""
    return ymap.CMapData.name.ToString()

# def ymap_exist_in_scene(new_ymap: str) -> bool:
#     """Checks if a YMAP already exists in the scene"""
#     new_ymap_bytes = Path.read_bytes(new_ymap)
#     ymap_list = dm.ymap_list
#     if ymap_list:
#         for ymap in ymap_list:
#             if ymap == new_ymap:
#                 return True
#     return False
            
def add_ymap_to_scene(new_ymap_path: str, self) -> bool:
    p = Path(new_ymap_path)
    filename = p.stem
    if dm.add_ymap(new_ymap_path):
        self.report({'INFO'}, f"YMAP {filename} added to scene")
        return True
    else:
        self.report({'ERROR'}, f"Error adding YMAP {filename} to scene")
        return False