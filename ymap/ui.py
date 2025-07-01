import bpy
from .operators import VICHO_OT_import_ymap, VICHO_OT_remove_ymap, VICHO_OT_go_to_entity
from ..vicho_dependencies import dependencies_manager as d
from ..vicho_operators import VICHO_OT_fake_op
from .operators_menu import (YMAP_MENU_OPERATORS_GROUPS)
from .constants import entity_flags_values, map_data_content_flags_values, map_data_flags_values
from ..icons_load import get_icon

class YMAPLIST_UL_list(bpy.types.UIList):
    bl_idname = "YMAPLIST_UL_list"
    
    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        scene = context.scene
        ymap_list = scene.ymap_list
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
        ymap_list = scene.ymap_list
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
        if d.available:
            row = layout.row()
            col = row.column(align=True)
            col.operator(VICHO_OT_import_ymap.bl_idname, text="", icon_value=get_icon("import_icon") )
            col.operator(VICHO_OT_fake_op.bl_idname, text="", icon_value=get_icon("export"))
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
                
                right_col = main_row.column()
                
                match ymap.active_category:
                    case "ymap.map_data_menu":
                        data_flow = right_col.grid_flow(row_major=True, columns=3, even_columns=True, even_rows=True, align=True)
                        data_flow.prop(ymap, "data_category", expand=True, icon_only=True)
                        right_col.separator()
                        match ymap.data_category:
                            case "DATA":
                                right_col.prop(ymap, "parent")
                            case "FLAGS":
                                right_col.label(text="Content Flags:")
                                content_flags_row = right_col.row()
                                cf_box = content_flags_row.box()
                                content_flags_grid = cf_box.grid_flow(row_major=True, columns=3, even_columns=True, even_rows=True, align=False)
                                for c_flag in map_data_content_flags_values:
                                    content_flags_grid.prop(ymap.content_flags, c_flag)
                                
                                right_col.separator()
                                flags_col = right_col.column()
                                flags_col.label(text="Flags:")
                                f_box = flags_col.box()
                                flags_grid = f_box.grid_flow(row_major=True, columns=1, even_columns=True, even_rows=True, align=False)
                                for flag in map_data_flags_values:
                                    flags_grid.prop(ymap.flags, flag)
                            case "EXTENTS":
                                right_col.prop(ymap, "show_streaming_extents", text="Show Streaming Extents", icon_value=get_icon("axis_arrow_info"))
                                right_col.prop(ymap, "show_entities_extents", text="Show Entity Extents", icon_value=get_icon("axis_arrow_info"))
                                
                                
                    case "ymap.entities_menu":
                        if ymap.entities:
                            right_col.template_list(
                                ENTITYLIST_UL_list.bl_idname, 
                                "", 
                                ymap, 
                                "entities", 
                                scene, 
                                "entity_list_index"
                            )
                            selected_ent = ymap.entities[scene.entity_list_index]
                            
                            right_col.separator()
                            row_ent_cat = right_col.row()
                            entity_data_flow = row_ent_cat.grid_flow(row_major=True, columns=5, even_columns=True, even_rows=True, align=True)
                            entity_data_flow.prop(selected_ent, "entity_data_toggle", expand=True, icon_only=True)
                            right_col.separator()
                            
                            match selected_ent.entity_data_toggle:
                                case "DATA":
                                    right_col.separator()
                                    obj_row = right_col.row(align=True)
                                    obj_box = obj_row.box()
                                    obj_box.separator(factor=0.1)
                                    ent_data_flow = obj_box.grid_flow(row_major=True, columns=1, even_columns=True, even_rows=True, align=False)
                                    ent_data_flow.prop(selected_ent, "guid")
                                    if selected_ent.linked_object:
                                        ent_data_flow.prop(selected_ent, "linked_object", icon="OBJECT_DATA")
                                        go_to_ent = ent_data_flow.operator(VICHO_OT_go_to_entity.bl_idname, icon="VIEWZOOM", text="")
                                    else:
                                        ent_data_flow.alert = True
                                        ent_data_flow.label(text="No linked object")

                                    
                                    
                                    
                                
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