import bpy

from . get_angle import GetAngle
from . get_edge import GetEdge
from . get_edge_menu import GetEdgeMenu

from . set_edge import SetEdge
from . set_edge_menu import SetEdgeMenu

from . edit_boolean import EditBoolean
from . edit_boolean_menu import EditBooleanMenu

from . object_boolean import ObjectBoolean
from . object_boolean_menu import ObjectBooleanMenu

from . auto_smooth import AutoSmooth
from . bevel_object import BevelObject
from . extra_menu import ExtraMenu

from . bedset_menu import BedsetMenu


bl_info = {
    "blender": (2, 80, 0),
    "name": "Bedset",
    "description": "Some tools to make Blender more comfortable",
    "author": "bonjorno7",
    "version": (0, 0, 8),
    "location": "3D View > Sidebar",
    "category": "Mesh",
    "warning": "",
}


classes = (
    GetAngle, GetEdge, GetEdgeMenu,
    SetEdge, SetEdgeMenu,
    EditBoolean, EditBooleanMenu,
    ObjectBoolean, ObjectBooleanMenu,
    AutoSmooth, BevelObject, ExtraMenu,
    BedsetMenu,
)


addon_keymaps = []


def remove_doubles_in_delete_menu(self, context):
    self.layout.separator()
    self.layout.operator("mesh.remove_doubles")


def register():
    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.VIEW3D_MT_edit_mesh_delete.append(remove_doubles_in_delete_menu)

    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')

    kmi_mnu = km.keymap_items.new("wm.call_menu", "Q", "PRESS", alt=True)
    kmi_mnu.properties.name = BedsetMenu.bl_idname
    addon_keymaps.append((km, kmi_mnu))


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

    bpy.types.VIEW3D_MT_edit_mesh_delete.remove(remove_doubles_in_delete_menu)

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()


if __name__ == "__main__":
    register()
