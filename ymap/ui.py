import bpy
from .operators import (VICHO_OT_import_ymap, 
                        VICHO_OT_remove_ymap, 
                        VICHO_OT_go_to_entity, 
                        VICHO_OT_add_ymap, 
                        VICHO_OT_add_entity,
                        VICHO_OT_add_entity_from_selection,
                        VICHO_OT_remove_entity,
                        VICHO_OT_export_ymap,
                        VICHO_OT_calculate_ymap_extents)
from ..vicho_dependencies import dependencies_manager as d
from ..vicho_operators import VICHO_OT_fake_op
from .operators_menu import (YMAP_MENU_OPERATORS_GROUPS)
from .constants import ENTITY_FLAGS_VALUES, MAP_DATA_CONTENT_FLAGS_VALUES, MAP_DATA_FLAGS_VALUES
from ..icons_load import get_icon
from .funcs import sanitize_name

class YMAPLIST_UL_list(bpy.types.UIList):
    bl_idname = "YMAPLIST_UL_list"
    
    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        scene = context.scene
        ymap_list = scene.ymap_list
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            if ymap_list:
                layout.prop(item, "enabled", text="", emboss=False, icon="CHECKBOX_HLT" if item.enabled else "CHECKBOX_DEHLT")
                layout.prop(item.ymap_object, "name", text="", emboss=False, icon_value=get_icon("island"))

class ENTITYLIST_UL_list(bpy.types.UIList):
    bl_idname = "ENTITYLIST_UL_list"
    
    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        scene = context.scene
        ymap_list = scene.ymap_list
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            if ymap_list:
                ymap = ymap_list[scene.ymap_list_index]
                entity = ymap.entities[index]
                if entity.linked_object:
                    layout.prop(item, "enabled", text="", emboss=False, icon="CHECKBOX_HLT" if item.enabled else "CHECKBOX_DEHLT")
                    layout.label(text=sanitize_name(entity.linked_object.name), icon_value=get_icon("home") if entity.is_mlo_instance else get_icon("nature_people"))
                else:
                    layout.label(text="Unassigned Entity", icon="ERROR")

    def filter_items(self, context, data, property):
        items = getattr(data, property)
        flt_flags = bpy.types.UI_UL_list.filter_items_by_name(self.filter_name, self.bitflag_filter_item, items, propname="archetype_name")
        return flt_flags, []
    
class GENERICNAME_UL_lists(bpy.types.UIList):
    bl_idname = "GENERICNAME_UL_lists"
    
    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        if self.layout_type in {"DEFAULT", "COMPACT"}:
                layout.prop(item, "name", text="", emboss=False, icon_value=get_icon("triangle"))

class YmapTools_PT_Panel(bpy.types.Panel):
    bl_label = "Map Data"
    bl_idname = "VICHOTOOLS_PT_Ymap"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Vicho's Tools"
    bl_options = {"DEFAULT_CLOSED"}
    
    def draw_header(self, context):
        self.layout.label(text="", icon_value=get_icon("database_marker"))

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        if d.available:
            row = layout.row()
            col = row.column(align=True)
            col.operator(VICHO_OT_import_ymap.bl_idname, text="", icon_value=get_icon("upload") )
            col.operator(VICHO_OT_export_ymap.bl_idname, text="", icon_value=get_icon("download"))
            col.separator()
            col.operator(VICHO_OT_add_ymap.bl_idname, text="", icon="ADD")
            col.operator(VICHO_OT_remove_ymap.bl_idname, text="", icon="REMOVE")
            col.separator()
            col.operator(
                VICHO_OT_fake_op.bl_idname,
                text="",
                icon="CURRENT_FILE",
            )
            row = row.row()
            col = row.column(align=False)
            col.scale_x = 1.2
            col.template_list(YMAPLIST_UL_list.bl_idname, "", scene, "ymap_list", scene, "ymap_list_index")
        else:
            layout.label(
                text="PythonNET or .NET 9 runtime aren't installed, please make sure you check the Add-on's preference menu",
                icon="ERROR",
            )

class YmapTools_Data_PT_Panel(bpy.types.Panel):
    bl_label = "Data"
    bl_idname = "VICHOTOOLS_PT_Ymap_Data"
    bl_parent_id = "VICHOTOOLS_PT_Ymap"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Vicho's Tools"
    
    @classmethod
    def poll(cls, context):
        return len(context.scene.ymap_list) > 0 and d.available
    
    def draw_header(self, context):
        self.layout.label(text="", icon_value=get_icon("sitemap"))
        
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        if d.available:
            ymap = scene.ymap_list[scene.ymap_list_index] if scene.ymap_list else None
            if ymap:
                main_row = layout.row()
                left_col = main_row.column()
                left_col.ui_units_x = 1
                left_col.alignment = 'CENTER'
                for op in YMAP_MENU_OPERATORS_GROUPS:
                    is_active = (op[0].bl_idname == ymap.active_category)
                    button_row = left_col.row()
                    op_button = button_row.operator(
                        op[0].bl_idname, 
                        text="", 
                        icon_value=get_icon(op[1]), 
                        emboss=is_active, 
                        depress=is_active
                    )
                    op_button.operator_id = op[0].bl_idname
                
                right_col = main_row.column(align=True)
                
                match ymap.active_category:
                    case "ymap.map_data_menu":
                        data_flow = right_col.grid_flow(row_major=True, columns=3, even_columns=True, even_rows=True, align=True)
                        data_flow.prop(ymap, "data_category", expand=True, icon_only=True, emboss=True)
                        ymap_data_box = right_col.box()
                        right_col.separator()
                        match ymap.data_category:
                            case "DATA":
                                ymap_data_box.prop(ymap, "parent")
                                ymap_data_box.separator(factor=23.4)
                            case "FLAGS":
                                content_flags_row = ymap_data_box.row()
                                cf_box = content_flags_row.box()
                                cf_box.label(text="Content Flags", icon="CHECKMARK")
                                content_flags_grid = cf_box.grid_flow(row_major=True, columns=2, even_columns=True, even_rows=True, align=False)
                                for c_flag in MAP_DATA_CONTENT_FLAGS_VALUES:
                                    content_flags_grid.alignment = 'CENTER'
                                    content_flags_grid.prop(ymap.content_flags, c_flag)
                                f_box = content_flags_row.box()
                                f_box.label(text="Flags", icon="CHECKMARK")
                                flags_grid = f_box.grid_flow(row_major=True, columns=2, even_columns=True, even_rows=True, align=False)
                                for flag in MAP_DATA_FLAGS_VALUES:
                                    flags_grid.alignment = 'CENTER'
                                    flags_grid.prop(ymap.flags, flag)
                                f_box.separator(factor=17)
                            case "EXTENTS":
                                ext_col = ymap_data_box.column(align=True)
                                ext_col.prop(ymap, "show_streaming_extents", text="Show Streaming Extents", icon_value=get_icon("axis_arrow_info"))
                                ext_col.prop(ymap, "show_entities_extents", text="Show Entity Extents", icon_value=get_icon("axis_arrow_info"))
                                ext_col.separator()
                                ext_col.operator(VICHO_OT_calculate_ymap_extents.bl_idname, text="Calculate Extents", icon="FILE_REFRESH")
                                ext_col.separator(factor=17)
                    case "ymap.entities_menu":
                        right_col.template_list(ENTITYLIST_UL_list.bl_idname, "", ymap, "entities", scene, "entity_list_index")
                        tool_ent_col = main_row.column(align=True)
                        tool_ent_col.ui_units_x = 1
                        tool_ent_col.operator(VICHO_OT_add_entity.bl_idname, text="", icon="ADD")
                        tool_ent_col.operator(VICHO_OT_remove_entity.bl_idname, text="", icon="REMOVE")
                        tool_ent_col.separator()
                        tool_ent_col.operator(VICHO_OT_add_entity_from_selection.bl_idname, text="", icon_value=get_icon("format_list_bulleted_type"))
                        selected_ent = ymap.entities[scene.entity_list_index] if ymap.entities else None
                        if selected_ent:
                            right_col.separator()
                            row_ent_cat = right_col.row(align=True)
                            entity_data_flow = row_ent_cat.grid_flow(row_major=True, columns=5, even_columns=True, even_rows=True, align=True)
                            entity_data_flow.prop(ymap, "entity_data_category", expand=True, icon_only=True, emboss=True)
                            entity_box = right_col.box()
                            col_box = entity_box.column(align=True)
                            match ymap.entity_data_category:
                                case "DATA":
                                    obj_row = col_box.row(align=True)
                                    ent_data_flow = obj_row.grid_flow(row_major=True, columns=1, even_columns=True, even_rows=True, align=False)
                                    if selected_ent.linked_object:
                                        ent_data_flow.prop(selected_ent, "linked_object", icon="OBJECT_DATA")
                                        ent_data_flow.operator(VICHO_OT_go_to_entity.bl_idname, icon="VIEWZOOM", text="")
                                    else:
                                        ent_data_flow.prop(selected_ent, "linked_object", icon="OBJECT_DATA")
                                case "FLAGS":
                                    entity_flags_flow = col_box.grid_flow(row_major=True, columns=4, even_columns=True, even_rows=False, align=False)
                                    for flag in ENTITY_FLAGS_VALUES:
                                        entity_flags_flow.prop(selected_ent.flags, flag)
                                    col_box.prop(selected_ent.flags, "total_flags", text="Total Flags", expand=False)
                                case "LOD":
                                    col_box.prop(selected_ent, "lod_level", text="")
                                    col_box.prop(selected_ent, "parent_index", text="Parent Index")
                                    col_box.prop(selected_ent, "lod_distance", text="LOD Distance")
                                    col_box.separator()
                                    col_box.prop(selected_ent, "child_lod_distance", text="Child Distance")
                                    col_box.prop(selected_ent, "num_children", text="Child Count")
                                case "MISC":
                                    col_box.prop(selected_ent, "ambient_occlusion_multiplier", text="AO Multiplier")
                                    col_box.prop(selected_ent, "artificial_ambient_occlusion", text="AO Artificial")
                                    col_box.separator()
                                    col_box.prop(selected_ent, "tint_value", text="Tint Value")
                                    col_box.prop(selected_ent, "priority_level", text="")
                                case "MLO":
                                    if selected_ent.is_mlo_instance:
                                        col_box.prop(selected_ent, "group_id", text="Group ID")
                                        col_box.prop(selected_ent, "floor_id", text="Floor ID")
                                        col_box.prop(selected_ent, "num_exit_portals", text="Exit Portals")
                                        col_box.prop(selected_ent, "mlo_inst_flags", text="Instance Flags")
                                        col_box.separator()

                                        header, panel = col_box.panel("tesd", default_closed=True)
                                        header.label(text="Default Entity Sets", icon_value=get_icon("shape"))
                                        if panel:
                                            panel_col = panel.column()
                                            panel_col.template_list(
                                                "GENERICNAME_UL_lists", 
                                                "", 
                                                selected_ent, 
                                                "default_entity_sets", 
                                                scene, 
                                                "default_entity_sets_index"
                                            )
                                            
                                    else:
                                        row_box = col_box.row(align=True)
                                        row_box.alignment = 'CENTER'
                                        row_box.label(text="Not an MLO Instance", icon="ERROR")
                    case "ymap.occluders_menu":
                        right_col.label(text="Occluders")
                    case "ymap.physics_dictionaries_menu":
                        right_col.label(text="Physics Dictionaries")
                    case "ymap.instanced_data_menu":
                        right_col.label(text="Instanced Data")
                    case "ymap.timecycle_modifiers_menu":
                        right_col.label(text="Timecycle Modifiers")
                    case "ymap.car_generators_menu":
                        right_col.label(text="Car Generators")
                    case "ymap.lod_lights_menu":
                        right_col.label(text="Lod Lights")
                    case "ymap.distant_lights_menu":
                        right_col.label(text="Distant Lights")