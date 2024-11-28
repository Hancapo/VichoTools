import bpy
from .operators import VICHO_OT_import_ymap, VICHO_OT_remove_ymap
from ..vicho_dependencies import dependencies_manager as d
from ..vicho_operators import VICHO_OT_fake_op

class YMAPLIST_UL_list(bpy.types.UIList):
    bl_idname = "YMAPLIST_UL_list"
    
    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        scene = context.scene
        ymap_list = scene.fake_ymap_list
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            if ymap_list:
                ymap = ymap_list[index]
                layout.prop(item, "enabled", text="", emboss=False, icon="CHECKBOX_HLT" if item.enabled else "CHECKBOX_DEHLT")
                layout.label(text=ymap.name, icon="OUTLINER_OB_GROUP_INSTANCE")


class ENTITYLIST_UL_list(bpy.types.UIList):
    bl_idname = "ENTITYLIST_UL_list"
    
    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        scene = context.scene
        ymap_list = scene.fake_ymap_list
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            if ymap_list:
                ymap = ymap_list[scene.ymap_list_index]
                entity = ymap.entities[index]
                layout.label(text=entity.archetype_name, icon="FILE_3D")
                
class YmapTools_PT_Panel(bpy.types.Panel):
    bl_label = "Map Data"
    bl_idname = "VICHOTOOLS_PT_Ymap"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Vicho's Tools"
    bl_options = {"DEFAULT_CLOSED"}
    
    def draw_header(self, context):
        self.layout.label(text="", icon="FORCE_MAGNETIC")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ymap_list = scene.fake_ymap_list
        
        if d.available:
            row = layout.row()
            col = row.column(align=True)
            col.operator(VICHO_OT_import_ymap.bl_idname, text="", icon="IMPORT")
            col.operator(VICHO_OT_import_ymap.bl_idname, text="", icon="EXPORT")
            col.separator()
            col.operator(VICHO_OT_fake_op.bl_idname, text="", icon="ADD")
            col.operator(VICHO_OT_remove_ymap.bl_idname, text="", icon="REMOVE")
            col.separator()
            col.operator(
                VICHO_OT_fake_op.bl_idname,
                text="",
                icon="CURRENT_FILE",
            )
            row = row.row()
            col = row.column(align=True)
            col.template_list(YMAPLIST_UL_list.bl_idname, "", scene, "fake_ymap_list", scene, "ymap_list_index")
            col = layout.column(align=True)
            row = col.row(align=True)
            if ymap_list:
                ymap = scene.fake_ymap_list[scene.ymap_list_index]
                if ymap is not None:
                    grid_row = row.grid_flow(row_major=True, columns=6, even_columns=False, even_rows=False, align=True)
                    grid_row.prop(scene, "data_type_toggle", icon="CON_ARMATURE", expand=True)
                    col.separator()
                    match scene.data_type_toggle:
                        case "MAPDATA":
                            grid_row = col.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                            grid_row.prop(ymap, "map_data_toggle", text="")
                                
                            box = col.box()
                            row = box.row(align=True)
                            match ymap.map_data_toggle:
                                case "DATA":
                                    col = row.column(align=True)
                                    col.prop(ymap, "name")
                                    col.prop(ymap, "parent")
                                case "CONTENT_FLAGS":
                                    col = row.column(align=True)
                                    grid_row = col.grid_flow(row_major=False, columns=6, even_columns=False, even_rows=False, align=True)
                                    grid_row.prop(ymap.content_flags, "hd", text="HD")
                                    grid_row.prop(ymap.content_flags, "lod", text="LOD")
                                    grid_row.prop(ymap.content_flags, "slod2_plus", text="SLOD2+")
                                    grid_row.prop(ymap.content_flags, "interior", text="Interior")
                                    grid_row.prop(ymap.content_flags, "slod", text="SLOD")
                                    grid_row.prop(ymap.content_flags, "occlusion", text="Occlusion")
                                    grid_row.prop(ymap.content_flags, "physics", text="Physics")
                                    grid_row.prop(ymap.content_flags, "lod_lights", text="LOD Lights")
                                    grid_row.prop(ymap.content_flags, "distant_lights", text="Distant Lights")
                                    grid_row.prop(ymap.content_flags, "critical", text="Critical")
                                    grid_row.prop(ymap.content_flags, "grass", text="Grass")
                                case "FLAGS":
                                    col = row.column(align=True)
                                    grid_row = col.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                                    grid_row.prop(ymap.flags, "script", text="Script")
                                    grid_row.prop(ymap.flags, "lod", text="LOD")
                                case "STREAMING_EXTENTS":
                                    col = row.column(align=True)
                                    col.prop(ymap, "streaming_extents_min", text="Min")
                                    col.prop(ymap, "streaming_extents_max", text="Max")
                                case "ENTITIES_EXTENTS":
                                    col = row.column(align=True)
                                    col.prop(ymap, "entities_extents_min", text="Min")
                                    col.prop(ymap, "entities_extents_max", text="Max")
                        case "ENTITIES":
                            box = col.box()
                            row = box.row(align=True)
                            if ymap.entities:
                                row.template_list(ENTITYLIST_UL_list.bl_idname, "", ymap, "entities", scene, "entity_list_index")
                                pass
                            else:
                                row.label(text="No entities found")
                                
                        case "OCCLUDERS":
                            box = col.box()
                            row = box.row(align=True)
                            row.label(text="Occluders Work in Progress")
                        case "PHYSICSDICTIONARIES":
                            box = col.box()
                            row = box.row(align=True)
                            row.label(text="Physics Dictionaries Work in Progress")
                        case "INSTANCEDDATA":
                            box = col.box()
                            row = box.row(align=True)
                            row.label(text="Instanced Data Work in Progress")
                        case "TIMECYCLEMODIFIERS":
                            box = col.box()
                            row = box.row(align=True)
                            row.label(text="Timecycle Modifiers Work in Progress")
                        case "CARGENERATORS":
                            box = col.box()
                            row = box.row(align=True)
                            row.label(text="Car Generators Work in Progress")
                        case "LODLIGHTS":
                            box = col.box()
                            row = box.row(align=True)
                            row.label(text="Lod Lights Work in Progress")
                        case "DISTANTLIGHTS":
                            box = col.box()
                            row = box.row(align=True)
                            row.label(text="Distant Lights Work in Progress")
                        case "BLOCK":
                            box = col.box()
                            row = box.row(align=True)
                            row.label(text="Block Work in Progress")
        else:
            layout.label(
                text="PythonNET or .NET 8 runtime aren't installed, please make sure you check the Add-on's preference menu",
                icon="ERROR",
            )
