import bpy
from . edit_boolean_menu import EditBooleanMenu
from . object_boolean_menu import ObjectBooleanMenu
from . get_edge_menu import GetEdgeMenu
from . set_edge_menu import SetEdgeMenu
from . extra_menu import ExtraMenu


class BedsetMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_BedsetMenu"
    bl_label = "Bedset"

    def draw(self, context):
        active = context.active_object

        if active is not None and active.mode == 'EDIT':
            self.layout.menu(EditBooleanMenu.bl_idname, icon='MOD_BOOLEAN')

            self.layout.separator()

            self.layout.menu(GetEdgeMenu.bl_idname, icon='EDGESEL')
            self.layout.menu(SetEdgeMenu.bl_idname, icon='EDGESEL')

        else:
            self.layout.menu(ObjectBooleanMenu.bl_idname, icon='MOD_BOOLEAN')

        self.layout.separator()

        self.layout.menu(ExtraMenu.bl_idname, icon='MONKEY')
