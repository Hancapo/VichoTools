from ..vicho_dependencies import dependencies_manager as dm
from pathlib import Path

def get_ymap_name(ymap) -> str:
    """Returns the name of the YMAP"""
    return ymap.CMapData.name.ToString()

def get_ymap_parent(ymap) -> str:
    """Returns the parent of the YMAP"""
    return ymap.CMapData.parent.ToString()

def get_ymap_flags(ymap) -> int:
    """Returns the flags of the YMAP"""
    return ymap.CMapData.flags

def get_ymap_content_flags(ymap) -> int:
    """Returns the content flags of the YMAP"""
    return ymap.CMapData.contentFlags

def get_ymap_streaming_extents_min(ymap) -> tuple[float, float, float]:
    """Returns the streaming extents min of the YMAP"""
    return (ymap.CMapData.streamingExtentsMin.X, ymap.CMapData.streamingExtentsMin.Y, ymap.CMapData.streamingExtentsMin.Z)

def get_ymap_streaming_extents_max(ymap) -> tuple[float, float, float]:
    """Returns the streaming extents max of the YMAP"""
    return (ymap.CMapData.streamingExtentsMax.X, ymap.CMapData.streamingExtentsMax.Y, ymap.CMapData.streamingExtentsMax.Z)

def get_ymap_entities_extents_min(ymap) -> tuple[float, float, float]:
    """Returns the entities extents min of the YMAP"""
    return (ymap.CMapData.entitiesExtentsMin.X, ymap.CMapData.entitiesExtentsMin.Y, ymap.CMapData.entitiesExtentsMin.Z)

def get_ymap_entities_extents_max(ymap) -> tuple[float, float, float]:
    """Returns the entities extents max of the YMAP"""
    return (ymap.CMapData.entitiesExtentsMax.X, ymap.CMapData.entitiesExtentsMax.Y, ymap.CMapData.entitiesExtentsMax.Z) 

# def ymap_exist_in_scene(new_ymap: str) -> bool:
#     """Checks if a YMAP already exists in the scene"""
#     new_ymap_bytes = Path.read_bytes(new_ymap)
#     ymap_list = dm.ymap_list
#     if ymap_list:
#         for ymap in ymap_list:
#             if ymap == new_ymap:
#                 return True
#     return False
            
def add_ymap_to_scene(scene, new_ymap_path: str, self) -> bool:
    p = Path(new_ymap_path)
    filename = p.stem
    if dm.add_ymap(new_ymap_path):
        new_fake_ymap = scene.fake_ymap_list.add()
        fill_data_from_ymap(scene, len(scene.fake_ymap_list) - 1)
        self.report({'INFO'}, f"YMAP {filename} added to scene")
        return True
    else:
        self.report({'ERROR'}, f"Error adding YMAP {filename} to scene")
        return False
    
def fill_data_from_ymap(scene, index) -> None:
    """Fills the data from the selected YMAP"""
    scene.fake_ymap_list[index].name = get_ymap_name(dm.get_ymap(index))
    scene.fake_ymap_list[index].parent = get_ymap_parent(dm.get_ymap(index))
    scene.fake_ymap_list[index].flags.total_flags = get_ymap_flags(dm.get_ymap(index))
    scene.fake_ymap_list[index].content_flags.total_flags = get_ymap_content_flags(dm.get_ymap(index))
    scene.fake_ymap_list[index].streaming_extents_min = get_ymap_streaming_extents_min(dm.get_ymap(index))
    scene.fake_ymap_list[index].streaming_extents_max = get_ymap_streaming_extents_max(dm.get_ymap(index))
    scene.fake_ymap_list[index].entities_extents_min = get_ymap_entities_extents_min(dm.get_ymap(index))
    scene.fake_ymap_list[index].entities_extents_max = get_ymap_entities_extents_max(dm.get_ymap(index))
    
def get_icon_and_name_from_toggle(item_list, scene) -> tuple[str, str]:
    """Returns the icon and name of the toggle"""
    get_selected_str = scene.data_type_toggle
    for item in item_list:
        if item[0] == get_selected_str:
            return item[2], item[3]