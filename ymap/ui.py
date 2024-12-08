import bpy
from .operators import VICHO_OT_import_ymap, VICHO_OT_remove_ymap, VICHO_OT_go_to_entity
from ..vicho_dependencies import dependencies_manager as d
from ..vicho_operators import VICHO_OT_fake_op
from .constants import entity_flags_values, map_data_content_flags_values, map_data_flags_values

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
                layout.prop(item, "enabled", text="", emboss=False, icon="CHECKBOX_HLT" if item.enabled else "CHECKBOX_DEHLT")
                layout.label(text=entity.archetype_name, icon="HOME" if entity.is_mlo_instance else "FILE_3D")
                
    def filter_items(self, context, data, property):
        items = getattr(data, property)
        flt_flags = bpy.types.UI_UL_list.filter_items_by_name(self.filter_name, self.bitflag_filter_item, items, propname="archetype_name")
        return flt_flags, []
                
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
            col.operator(VICHO_OT_fake_op.bl_idname, text="", icon="EXPORT")
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
                                    grid_row = col.grid_flow(row_major=False, columns=2, even_columns=False, even_rows=False, align=True)
                                    for flag in map_data_content_flags_values:
                                        grid_row.prop(ymap.content_flags, flag)
                                case "FLAGS":
                                    col = row.column(align=True)
                                    grid_row = col.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                                    for flags in map_data_flags_values:
                                        grid_row.prop(ymap.flags, flags)
                                case "EXTENTS":
                                    header, panel = box.panel("_streaming_extents", default_closed=False)
                                    header.label(text="Streaming")
                                    if panel:
                                        col = panel.column(align=True)
                                        col.prop(ymap, "streaming_extents_min", text="Min")
                                        col.prop(ymap, "streaming_extents_max", text="Max")
                                        col.separator()
                                        col.prop(ymap, "show_streaming_extents", text="Show Gizmo", icon="META_CUBE")
                                    header, panel = box.panel("_entities_extents", default_closed=False)
                                    header.label(text="Entities")
                                    if panel:
                                        col = panel.column(align=True)
                                        col.prop(ymap, "entities_extents_min", text="Min")
                                        col.prop(ymap, "entities_extents_max", text="Max")
                                        col.separator()
                                        col.prop(ymap, "show_entities_extents", text="Show Gizmo", icon="META_CUBE")
                                    
                        case "ENTITIES":
                            box = col.box()
                            row = box.row(align=True)
                            if ymap.entities:
                                row.template_list(ENTITYLIST_UL_list.bl_idname, "", ymap, "entities", scene, "entity_list_index")
                                selected_entity = ymap.entities[scene.entity_list_index]
                                col.separator()
                                grid_row = col.grid_flow(row_major=True, columns=6, even_columns=False, even_rows=False, align=True)
                                grid_row.prop(selected_entity, "entity_data_toggle", text="")
                                box = col.box()
                                row = box.row(align=True)
                                match selected_entity.entity_data_toggle:
                                    case "DATA":
                                        col = row.column(align=True)
                                        col.prop(selected_entity, "type")
                                        col.prop(selected_entity, "archetype_name")
                                        col.prop(selected_entity, "guid")
                                        col.separator()
                                        row = col.row(align=True)
                                        row.prop(selected_entity, "linked_object")
                                        row.operator(VICHO_OT_go_to_entity.bl_idname, text="", icon="VIEWZOOM")
                                    case "FLAGS":
                                        col = row.column(align=True)
                                        grid_row = col.grid_flow(row_major=False, columns=2, even_columns=False, even_rows=False, align=True)
                                        for flag in entity_flags_values:
                                            grid_row.prop(selected_entity.flags, flag)
                                    case "LOD":
                                        col = row.column(align=True)
                                        col.prop(selected_entity, "lod_distance")
                                        col.prop(selected_entity, "child_lod_distance")
                                        col.prop(selected_entity, "num_children")
                                        col.separator()
                                        col.prop(selected_entity, "lod_level")
                                    case "AMBIENT_OCCLUSION":
                                        col = row.column(align=True)
                                        col.prop(selected_entity, "ambient_occlusion_multiplier", text="Multiplier")
                                        col.prop(selected_entity, "artificial_ambient_occlusion", text="Artificial")
                                    case "MLO":
                                        col = row.column(align=True)
                                        if selected_entity.is_mlo_instance:
                                            col.label(text="It's a MLO Instance")
                                        else:
                                            col.label(text="Not a MLO Instance", icon="ERROR")
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
        else:
            layout.label(
                text="PythonNET or .NET 8 runtime aren't installed, please make sure you check the Add-on's preference menu",
                icon="ERROR",
            )
