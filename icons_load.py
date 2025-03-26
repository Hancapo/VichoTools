import bpy
import os
from bpy.utils import previews

pcoll = None
preview_collections = {}

def init_icons():
    """Initializes the icon collections."""
    global pcoll, preview_collections
    if preview_collections:
        for coll in preview_collections.values():
            bpy.utils.previews.remove(coll)
        preview_collections.clear()
    
    pcoll = previews.new()
    preview_collections["main"] = pcoll
    return pcoll

def ensure_icons_loaded():
    """Checks if the icons are loaded, and if not, loads them."""
    global pcoll, preview_collections
    if pcoll is None or not preview_collections.get("main"):
        init_icons()
        load_icons()
    return pcoll

def load_icons():
    """Loads all custom icons."""
    global pcoll
    
    if pcoll is None:
        init_icons()
    
    icons_dir = os.path.join(os.path.dirname(__file__), "icons")
    print(f"Loading icons from: {icons_dir}")
    
    icons = [
        ["map_legend", "map_legend.png"],
        ["car_multiple", "car_multiple.png"],
        ["vector_diff", "vector_diff.png"],
        ["forest", "forest.png"],
        ["home_city", "home_city.png"],
        ["arrow_collapse_vertical", "arrow_collapse_vertical.png"],
        ["grass", "grass.png"],
        ["sun_clock", "sun_clock.png"],
        ["lamps", "lamps.png"],
        ["lighthouse_on", "lighthouse_on.png"],
        ["file_import", "file_import.png"],
        ["map_plus", "map_plus.png"],
        ["map_minus", "map_minus.png"],
        ["export", "export.png"],
        ["import_icon", "import.png"],
        ["box_shadow", "box_shadow.png"],
        ["sitemap", "sitemap.png"],
        ["axis_arrow_info", "axis_arrow_info.png"],
        ["alpha_x_box", "alpha_x_box.png"],
    ]
    
    for name, filename in icons:
        if name in pcoll:
            print(f"Icon '{name}' already exists, skipping")
            continue
            
        icon_path = os.path.join(icons_dir, filename)
        if os.path.exists(icon_path):
            pcoll.load(name, icon_path, 'IMAGE')
        else:
            print(f"Icon not found: {icon_path}")
    
    print(f"Loaded icons: {list(pcoll.keys())}")
    return pcoll

def get_icon(icon_name, fallback="QUESTION"):
    """Safely obtains an icon ID."""
    global pcoll
    ensure_icons_loaded()
    try:
        return pcoll[icon_name].icon_id
    except (KeyError, AttributeError):
        print(f"Warning: Icon '{icon_name}' not found, using fallback")
        return fallback

def unregister_icons():
    """Removes all icon collections."""
    global pcoll, preview_collections
    for coll in preview_collections.values():
        bpy.utils.previews.remove(coll)
    preview_collections.clear()
    pcoll = None