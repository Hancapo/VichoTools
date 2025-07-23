import bpy

class getYmapData:
    def get_ymap_data(self, context):
        ymap = context.scene.ymap_list[context.scene.ymap_list_index]
        if ymap:
            return ymap
        return None


class MAPDATA_Menu_OT_Operator(bpy.types.Operator, getYmapData):
    bl_idname = "ymap.map_data_menu"
    bl_label = "Map Data Menu"
    bl_description = "Where all the map data is stored"
    bl_options = {"UNDO"}
    
    operator_id: bpy.props.StringProperty() # type: ignore
    
    def execute(self, context):
        ymap = self.get_ymap_data(context)
        if ymap:
            ymap.active_category = self.operator_id
        print("Debug: Executing Map Data Menu operator")
        return {"FINISHED"}
    
class ENTITIES_Menu_OT_Operator(bpy.types.Operator, getYmapData):
    bl_idname = "ymap.entities_menu"
    bl_label = "Entities Menu"
    bl_description = "Where all the entities are stored"
    bl_options = {"UNDO"}
    
    operator_id: bpy.props.StringProperty() # type: ignore
    
    def execute(self, context):
        ymap = self.get_ymap_data(context)
        if ymap:
            ymap.active_category = self.operator_id
        return {"FINISHED"}
    
class OCCLUDERS_Menu_OT_Operator(bpy.types.Operator, getYmapData):
    bl_idname = "ymap.occluders_menu"
    bl_label = "Occluders Menu"
    bl_description = "Where all the occluders are stored"
    bl_options = {"UNDO"}
    
    operator_id: bpy.props.StringProperty() # type: ignore
    
    def execute(self, context):
        ymap = self.get_ymap_data(context)
        if ymap:
            ymap.active_category = self.operator_id
        return {"FINISHED"}
    
class PHYSICSDICTIONARIES_Menu_OT_Operator(bpy.types.Operator, getYmapData):
    bl_idname = "ymap.physics_dictionaries_menu"
    bl_label = "Physics Dictionaries Menu"
    bl_description = "Where all the physics dictionaries are stored"
    bl_options = {"UNDO"}
    
    operator_id: bpy.props.StringProperty() # type: ignore
    
    def execute(self, context):
        ymap = self.get_ymap_data(context)
        if ymap:
            ymap.active_category = self.operator_id
        return {"FINISHED"}
    
class INSTANCEDDATA_Menu_OT_Operator(bpy.types.Operator, getYmapData):
    bl_idname = "ymap.instanced_data_menu"
    bl_label = "Instanced Data Menu"
    bl_description = "Where all the instanced data is stored"
    bl_options = {"UNDO"}
    
    operator_id: bpy.props.StringProperty() # type: ignore
    
    def execute(self, context):
        ymap = self.get_ymap_data(context)
        if ymap:
            ymap.active_category = self.operator_id
        return {"FINISHED"}
    
class TIMECYCLEMODIFIERS_Menu_OT_Operator(bpy.types.Operator, getYmapData):
    bl_idname = "ymap.timecycle_modifiers_menu"
    bl_label = "Timecycle Modifiers Menu"
    bl_description = "Where all the timecycle modifiers are stored"
    bl_options = {"UNDO"}
    
    operator_id: bpy.props.StringProperty() # type: ignore
    
    def execute(self, context):
        ymap = self.get_ymap_data(context)
        if ymap:
            ymap.active_category = self.operator_id
        return {"FINISHED"}
    
class CARGENERATORS_Menu_OT_Operator(bpy.types.Operator, getYmapData):
    bl_idname = "ymap.car_generators_menu"
    bl_label = "Car Generators Menu"
    bl_description = "Where all the car generators are stored"
    bl_options = {"UNDO"}
    
    operator_id: bpy.props.StringProperty() # type: ignore
    
    def execute(self, context):
        ymap = self.get_ymap_data(context)
        if ymap:
            ymap.active_category = self.operator_id
        return {"FINISHED"}

class LODLIGHTS_Menu_OT_Operator(bpy.types.Operator, getYmapData):
    bl_idname = "ymap.lod_lights_menu"
    bl_label = "Lod Lights Menu"
    bl_description = "Where all the lod lights are stored"
    bl_options = {"UNDO"}
    
    operator_id: bpy.props.StringProperty() # type: ignore
    
    def execute(self, context):
        ymap = self.get_ymap_data(context)
        if ymap:
            ymap.active_category = self.operator_id
        return {"FINISHED"}
    
class DISTANTLIGHTS_Menu_OT_Operator(bpy.types.Operator, getYmapData):
    bl_idname = "ymap.distant_lights_menu"
    bl_label = "Distant Lights Menu"
    bl_description = "Where all the distant lights are stored"
    bl_options = {"UNDO"}
    
    operator_id: bpy.props.StringProperty() # type: ignore
    
    def execute(self, context):
        ymap = self.get_ymap_data(context)
        if ymap:
            ymap.active_category = self.operator_id
        return {"FINISHED"}


YMAP_MENU_OPERATORS_GROUPS = [
    (MAPDATA_Menu_OT_Operator, "map_legend"),
    (ENTITIES_Menu_OT_Operator, "home_city"),
    (OCCLUDERS_Menu_OT_Operator, "vector_diff"),
    (PHYSICSDICTIONARIES_Menu_OT_Operator, "arrow_collapse_vertical"),
    (INSTANCEDDATA_Menu_OT_Operator, "grass"),
    (TIMECYCLEMODIFIERS_Menu_OT_Operator, "sun_clock"),
    (CARGENERATORS_Menu_OT_Operator, "car_multiple"),
    (LODLIGHTS_Menu_OT_Operator, "lamps"),
    (DISTANTLIGHTS_Menu_OT_Operator, "lighthouse_on")
]