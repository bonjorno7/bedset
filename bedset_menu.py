import bpy
from . edit_boolean_menu import EditBooleanMenu
from . get_edge_menu import GetEdgeMenu
from . set_edge_menu import SetEdgeMenu
from . extra_menu import ExtraMenu


class BedsetMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_BedsetMenu"
    bl_label = "Bedset"

    def draw(self, context):
        edit = context.active_object.mode == "EDIT"

        if edit:
            self.layout.menu(EditBooleanMenu.bl_idname, icon='MOD_BOOLEAN')
            self.layout.separator()
            self.layout.menu(GetEdgeMenu.bl_idname, icon='EDGESEL')
            self.layout.menu(SetEdgeMenu.bl_idname, icon='EDGESEL')
            self.layout.separator()

        else:
            pass

        self.layout.menu(ExtraMenu.bl_idname, icon='MOD_BOOLEAN')
