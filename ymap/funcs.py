from ..vicho_dependencies import dependencies_manager as dm
from pathlib import Path
from .helper import get_hash_from_bytes

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

def ymap_exist_in_scene(scene, new_ymap: str) -> bool:
    """Checks if a YMAP already exists in the scene"""
    p: Path = Path(new_ymap)
    new_ymap_bytes: bytes = p.read_bytes()
    new_ymap_bytes_hash: str = get_hash_from_bytes(new_ymap_bytes)
    ymap_list = scene.fake_ymap_list
    if len(ymap_list) > 0:
        for ymap in ymap_list:
            print(f"YMAP HASH: {ymap.hash} NEW HASH: {new_ymap_bytes_hash}")
            if ymap.hash == new_ymap_bytes_hash:
                return True
    return False
            
def add_ymap_to_scene(scene, new_ymap_path: str, self) -> bool:
    p: Path = Path(new_ymap_path)
    filename = p.stem
    if not ymap_exist_in_scene(scene, new_ymap_path):
        if dm.add_ymap(new_ymap_path):
            new_fake_ymap = scene.fake_ymap_list.add()
            fill_data_from_ymap(scene, len(scene.fake_ymap_list) - 1)
            self.report({'INFO'}, f"YMAP {filename} added to scene")
            return True
        else:
            self.report({'ERROR'}, f"Error adding YMAP {filename} to scene")
            return False
    else:
        self.report({'ERROR'}, f"YMAP {filename} already exists in scene")
        return False
 
def remove_ymap_from_scene(scene, index: int) -> bool:
    """Removes a YMAP from the scene"""
    if dm.remove_ymap(index):
        scene.fake_ymap_list.remove(index)
        scene.ymap_list_index = len(scene.fake_ymap_list) - 1
        return True
    return False
    
def fill_data_from_ymap(scene, index: int) -> None:
    """Fills the data from the selected YMAP"""
    scene.fake_ymap_list[index].name = get_ymap_name(dm.get_ymap(index))
    scene.fake_ymap_list[index].parent = get_ymap_parent(dm.get_ymap(index))
    scene.fake_ymap_list[index].flags.total_flags = get_ymap_flags(dm.get_ymap(index))
    scene.fake_ymap_list[index].content_flags.total_flags = get_ymap_content_flags(dm.get_ymap(index))
    scene.fake_ymap_list[index].streaming_extents_min = get_ymap_streaming_extents_min(dm.get_ymap(index))
    scene.fake_ymap_list[index].streaming_extents_max = get_ymap_streaming_extents_max(dm.get_ymap(index))
    scene.fake_ymap_list[index].entities_extents_min = get_ymap_entities_extents_min(dm.get_ymap(index))
    scene.fake_ymap_list[index].entities_extents_max = get_ymap_entities_extents_max(dm.get_ymap(index))
    scene.fake_ymap_list[index].hash = get_hash_from_bytes(dm.get_ymap_bytes(index))
    
def get_icon_and_name_from_toggle(item_list, scene) -> tuple[str, str]:
    """Returns the icon and name of the toggle"""
    get_selected_str = scene.data_type_toggle
    for item in item_list:
        if item[0] == get_selected_str:
            return item[2], item[3]