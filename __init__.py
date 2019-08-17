import bpy

from . booleans . edit import EditBoolean
from . booleans . mod import ModBoolean

from . modifiers . bevel import Bevel
from . modifiers . solidify import Solidify
from . modifiers . apply import Apply

from . other . auto_smooth import AutoSmooth
from . other . export_obj import ExportObj

from . edges . get_angle import GetAngle
from . edges . get_edge import GetEdge
from . edges . set_edge import SetEdge

from . other . bake import BakeSettings
from . other . bake import Bake
from . other . bake import BakePanel

from . menus import *


bl_info = {
    "blender": (2, 80, 0),
    "name": "Bedset",
    "description": "Some tools to make Blender more comfortable",
    "author": "bonjorno7",
    "version": (0, 1, 4),
    "location": "3D View > Sidebar",
    "category": "Mesh",
    "warning": "",
}


classes = (
    BakeSettings, Bake, BakePanel,
    ModBoolean, EditBoolean,
    GetAngle, GetEdge, SetEdge,
    Bevel, Solidify, Apply,
    AutoSmooth, ExportObj,
    BooleansMenu, CallBooleansMenu,
    ModifiersMenu, CallModifiersMenu,
    OtherMenu, CallOtherMenu,
    SelectEdgesMenu, CallSelectEdgesMenu,
    SelectEdgesInvertedMenu, CallSelectEdgesInvertedMenu,
    MarkEdgesMenu, CallMarkEdgesMenu,
    ClearEdgesMenu, CallClearEdgesMenu,
    EdgesMenu, CallEdgesMenu,
    BedsetMenu,
)


addon_keymaps = []


def remove_doubles_in_delete_menu(self, context):
    self.layout.separator()
    self.layout.operator("mesh.remove_doubles")


def register():
    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.BedsetBakeSettings = bpy.props.PointerProperty(type=BakeSettings)

    bpy.types.VIEW3D_MT_edit_mesh_delete.append(remove_doubles_in_delete_menu)

    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name="3D View", space_type='VIEW_3D')

    kmi_mnu = km.keymap_items.new("wm.call_menu_pie", "B", 'PRESS')
    kmi_mnu.properties.name = BedsetMenu.bl_idname
    addon_keymaps.append((km, kmi_mnu))


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

    del bpy.types.Scene.BedsetBakeSettings

    bpy.types.VIEW3D_MT_edit_mesh_delete.remove(remove_doubles_in_delete_menu)

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()


if __name__ == "__main__":
    register()
