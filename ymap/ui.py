import bpy
from .operators import VICHO_OT_import_ymap
from .funcs import get_icon_and_name_from_toggle
from .properties import YMAP_TYPE_TOGGLES

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
        col = layout.column(align=True)
        col.operator(VICHO_OT_import_ymap.bl_idname, text="Import YMAP(s)")
        col.separator()
        col.template_list(YMAPLIST_UL_list.bl_idname, "", scene, "fake_ymap_list", scene, "ymap_list_index")
        col = layout.column(align=True)
        row = col.row(align=True)
        
        
        if ymap_list:
            ymap = scene.fake_ymap_list[scene.ymap_list_index]
            if ymap is not None:
                grid_row = row.grid_flow(row_major=True, columns=6, even_columns=False, even_rows=False, align=True)
                grid_row.prop(scene, "data_type_toggle", icon="CON_ARMATURE", expand=True)
                header, panel = layout.panel("ymap_current_data_tab", default_closed=True)
                tab_name, tab_icon = get_icon_and_name_from_toggle(YMAP_TYPE_TOGGLES, scene)
                header.label(text=tab_name, icon=tab_icon)
                
                if panel:
                    match scene.data_type_toggle:
                        case "MAPDATA":
                            box = panel.box()
                            row = box.row(align=True)
                            col = row.column(align=True)
                            col.prop(ymap, "name")
                            col.prop(ymap, "parent")
                            col.prop(ymap, "flags")
                            col.prop(ymap, "content_flags")
                            col.prop(ymap, "streaming_extents_min")
                            col.prop(ymap, "streaming_extents_max")
                            col.prop(ymap, "entities_extents_min")
                            col.prop(ymap, "entities_extents_max")
                        # case "ENTITIES":
                        #     box = panel.box()
                        #     row = box.row(align=True)
                        #     col = row.column(align=True)
                        #     col.label(text="Entities")
                        # case "OCCLUDERS":
                        #     box = panel.box()
                        #     row = box.row(align=True)
                        #     col = row.column(align=True)
                        #     col.label(text="Occluders")
                        # case "PHYSICSDICTIONARIES":
                        #     box = panel.box()
                        #     row = box.row(align=True)
                        #     col = row.column(align=True)
                        #     col.label(text="Physics Dictionaries")
                        # case "INSTANCEDDATA":
                        #     box = panel.box()
                        #     row = box.row(align=True)
                        #     col = row.column(align=True)
                        #     col.label(text="Instanced Data")
                        # case "TIMECYCLEMODIFIERS":
                        #     box = panel.box()
                        #     row = box.row(align=True)
                        #     col = row.column(align=True)
                        #     col.label(text="Timecycle Modifiers")
                        # case "CARGENERATORS":
                        #     box = panel.box()
                        #     row = box.row(align=True)
                        #     col = row.column(align=True)
                        #     col.label(text="Car Generators")
                        # case "LODLIGHTS":
                        #     box = panel.box()
                        #     row = box.row(align=True)
                        #     col = row.column(align=True)
                        #     col.label(text="Lod Lights")
                        # case "DISTANTLIGHTS":
                        #     box = panel.box()
                        #     row = box.row(align=True)
                        #     col = row.column(align=True)
                        #     col.label(text="Distant Lights")
                        # case "BLOCK":
                        #     box = panel.box()
                        #     row = box.row(align=True)
                        #     col = row.column(align=True)
                        #     col.label(text="Block")
        
        # if ymap_list:
        #     ymap = scene.fake_ymap_list[scene.ymap_list_index]
        #     if ymap is not None:
        #         header, panel = layout.panel("ymap_data", default_closed=True)
        #         header.label(text="Data", icon="INFO_LARGE")
        #         if panel:
        #             box = panel.box()
        #             row = box.row(align=True)
        #             col = row.column(align=True)
        #             col.prop(ymap, "name")
        #             col.prop(ymap, "parent")
        #             col.prop(ymap, "flags")
        #             col.prop(ymap, "content_flags")
        #             col.prop(ymap, "streaming_extents_min")
        #             col.prop(ymap, "streaming_extents_max")
        #             col.prop(ymap, "entities_extents_min")
        #             col.prop(ymap, "entities_extents_max")
                    
        #col.prop(bpy.context.scene, "ymap_assets_path")
