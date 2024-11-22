










def ymap_exist_in_list(list, ymap):
    for item in list:
        if item.name == ymap.name:
            return True
    return False

def add_ymap_to_list(scene, ymap, self=None):
    if not ymap_exist_in_list(scene.ymap_list, ymap):
        ymap_item = scene.ymap_list.add()
        ymap_item.name = ymap.name