import bpy
from .operators.operators_entity import VICHO_OT_select_all_entities, VICHO_OT_deselect_all_entities

addon_keymaps = []

def register():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    
    if not kc:
        return

    km = kc.keymaps.get("Window")
    if not km:
        km = kc.keymaps.new(name="Window", space_type='WINDOW')

    kmi = km.keymap_items.new(VICHO_OT_select_all_entities.bl_idname, 'A', 'PRESS', ctrl=True)
    addon_keymaps.append((km, kmi))

    kmi = km.keymap_items.new(VICHO_OT_deselect_all_entities.bl_idname, 'ESC', 'PRESS')
    addon_keymaps.append((km, kmi))

def unregister():
    for km, kmi in addon_keymaps:
        try:
            km.keymap_items.remove(kmi)
        except (KeyError, ValueError, AttributeError):
            pass
    addon_keymaps.clear()