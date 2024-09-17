import bpy
from bpy.types import Context
from .operators import Import_YNV

class VichoNavmeshesTools_PT_Panel(bpy.types.Panel):
    bl_label = "Navmeshes"
    bl_idname = "VICHOTOOLS_PT_Navmeshes"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Vicho's Tools"
    bl_options = {"DEFAULT_CLOSED"}
    
    def draw_header(self, context: Context):
        self.layout.label(text="", icon="VIEW_PERSPECTIVE")
        
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        row = layout.row()
        col = row.column()
        col.operator(Import_YNV.bl_idname, text="Import YNV(s)", icon="IMPORT")



class VichoTypeObject_PT_Panel(bpy.types.Panel):
    bl_label = "Vicho's Tools"
    bl_idname = "VICHOTOOLS_PT_VichoTypeObject"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col = row.column()
        col.prop(context.object, "vicho_type")
        col.separator()
        
        if context.object.vicho_type == "vicho_nav_mesh":
            col.prop(context.object.navmesh_properties, "AreaID")
            col.prop(context.object.navmesh_properties, "UnkHash")
            box = col.box()
            box.label(text="Content Flags")
            row = box.row()
            col = row.column()
            col.prop(context.object.navmesh_properties.ContentFlags, "Polygons")
            col.prop(context.object.navmesh_properties.ContentFlags, "Portals")
            col.prop(context.object.navmesh_properties.ContentFlags, "Vehicle")
            col.prop(context.object.navmesh_properties.ContentFlags, "Unknown8")
            col.prop(context.object.navmesh_properties.ContentFlags, "Unknown16")
        if context.object.vicho_type == "vicho_nav_point":
            col.prop(context.object.navpoint_properties, "Type")
            
class VichoMaterial_PT_Panel(bpy.types.Panel):
    bl_label = "Vicho's Tools"
    bl_idname = "VICHOTOOLS_PT_VichoMaterial"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"
    
    def draw(self, context: Context):
        layout = self.layout
        
        # Crear una fila para poner las cajas en columnas
        row = layout.row()
        
        # Columna 1 (Flags 1)
        col1 = row.column()
        box1 = col1.box()
        box1.label(text="Flags 1")
        box1.prop(context.material.NavPolyFlagsA, "SmallPoly", text="Small Poly")
        box1.prop(context.material.NavPolyFlagsA, "LargePoly", text="Large Poly")
        box1.prop(context.material.NavPolyFlagsA, "IsPavement", text="Is Pavement")
        box1.prop(context.material.NavPolyFlagsA, "IsUnderground", text="Is Underground")
        box1.prop(context.material.NavPolyFlagsA, "Unused1", text="Unused 1")
        box1.prop(context.material.NavPolyFlagsA, "Unused2", text="Unused 2")
        box1.prop(context.material.NavPolyFlagsA, "IsTooSteepToWalk", text="Is Too Steep To Walk")
        box1.prop(context.material.NavPolyFlagsA, "IsWater", text="Is Water")

        # Columna 2 (Flags 2)
        col2 = row.column()
        box2 = col2.box()
        box2.label(text="Flags 2")
        box2.prop(context.material.NavPolyFlagsB, "AudioProperties1", text="Audio Properties 1")
        box2.prop(context.material.NavPolyFlagsB, "AudioProperties2", text="Audio Properties 2")
        box2.prop(context.material.NavPolyFlagsB, "AudioProperties3", text="Audio Properties 3")
        box2.prop(context.material.NavPolyFlagsB, "AudioProperties4", text="Audio Properties 4")
        box2.prop(context.material.NavPolyFlagsB, "Unused3", text="Unused 3")
        box2.prop(context.material.NavPolyFlagsB, "NearCarNode", text="Near Car Node")
        box2.prop(context.material.NavPolyFlagsB, "IsInterior", text="Is Interior")
        box2.prop(context.material.NavPolyFlagsB, "IsIsolated", text="Is Isolated")
        
        # Columna 3 (Flags 3)
        col3 = row.column()
        box3 = col3.box()
        box3.label(text="Flags 3")
        box3.prop(context.material.NavPolyFlagsC, "ZeroAreaStitchPoly", text="Zero Area Stitch Poly")
        box3.prop(context.material.NavPolyFlagsC, "CanSpawnPeds", text="Can Spawn Peds")
        box3.prop(context.material.NavPolyFlagsC, "IsRoad", text="Is Road")
        box3.prop(context.material.NavPolyFlagsC, "LiesAlongEdgeOfMesh", text="Lies Along Edge Of Mesh")
        box3.prop(context.material.NavPolyFlagsC, "IsTraintrack", text="Is Traintrack")
        box3.prop(context.material.NavPolyFlagsC, "IsShallowWater", text="Is Shallow Water")
        box3.prop(context.material.NavPolyFlagsC, "PedDensity1", text="Ped Density 1")
        box3.prop(context.material.NavPolyFlagsC, "PedDensity2", text="Ped Density 2")
        box3.prop(context.material.NavPolyFlagsC, "PedDensity3", text="Ped Density 3")
        
        # Columna 4 (Flags 4)
        col4 = row.column()
        box4 = col4.box()
        box4.label(text="Flags 4")
        box4.prop(context.material.NavPolyFlagsD, "CoverSouth", text="Cover South")
        box4.prop(context.material.NavPolyFlagsD, "CoverSouthEast", text="Cover South East")
        box4.prop(context.material.NavPolyFlagsD, "CoverEast", text="Cover East")
        box4.prop(context.material.NavPolyFlagsD, "CoverNorthEast", text="Cover North East")
        box4.prop(context.material.NavPolyFlagsD, "CoverNorth", text="Cover North")
        box4.prop(context.material.NavPolyFlagsD, "CoverNorthWest", text="Cover North West")
        box4.prop(context.material.NavPolyFlagsD, "CoverWest", text="Cover West")
        box4.prop(context.material.NavPolyFlagsD, "CoverSouthWest", text="Cover South West")
        
        
        