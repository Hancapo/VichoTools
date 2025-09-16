import bpy
from .operators.operators_entity import VICHO_OT_select_all_entities

class KeymapManager:
    _keymaps = []
    
    @classmethod
    def register_keymaps(cls):
        wm = bpy.context.window_manager
        
        kc = wm.keyconfigs.default
        
        if kc:
            km = kc.keymaps.new(name="User Interface", space_type='EMPTY', region_type='UI')
            kmi = km.keymap_items.new(VICHO_OT_select_all_entities.bl_idname, 'A', 'PRESS', ctrl=True)
            cls._keymaps.append((km, kmi))
            
    @classmethod
    def unregister_keymaps(cls):
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.default
        if kc:
            for km, kmi in cls._keymaps:
                try:
                    km.keymap_items.remove(kmi)
                except:
                    pass
        cls._keymaps.clear()
        
def register():
    KeymapManager.register_keymaps()
    
def unregister():
    KeymapManager.unregister_keymaps()