import bpy

from . auto_smooth import AutoSmooth
from . mod_boolean import ModBoolean
from . edit_boolean import EditBoolean

from . get_angle import GetAngle
from . get_edge import GetEdge
from . set_edge import SetEdge

from . menus import *


bl_info = {
    "blender": (2, 80, 0),
    "name": "Bedset",
    "description": "Some tools to make Blender more comfortable",
    "author": "bonjorno7",
    "version": (0, 1, 7),
    "location": "3D View",
    "category": "Mesh",
    "warning": "",
}


classes = (
    AutoSmooth, ModBoolean, EditBoolean,
    GetAngle, GetEdge, SetEdge,
    ViewPie, ShadingPie,
    ApplyPie, OriginPie,
    BedsetPie, ModBooleanPie, 
    EditBooleanPie, DeletePie,
    EdgeSelectMenu, EdgeMarkMenu, FaceSelectMenu,
    VertexPie, EdgePie, FacePie,
)


addon_keymaps = []


def register():
    for c in classes:
        bpy.utils.register_class(c)

    kc = bpy.context.window_manager.keyconfigs.addon
    kmo = kc.keymaps.new(name="Object Mode", space_type='EMPTY')
    kmm = kc.keymaps.new(name="Mesh", space_type='EMPTY')

    kmi = kmo.keymap_items.new("wm.call_menu_pie", 'B', 'PRESS')
    kmi.properties.name = BedsetPie.bl_idname
    addon_keymaps.append((kmo, kmi))

    kmi = kmo.keymap_items.new("wm.call_menu_pie", 'B', 'PRESS', shift=True)
    kmi.properties.name = ModBooleanPie.bl_idname
    addon_keymaps.append((kmo, kmi))

    kmi = kmm.keymap_items.new("wm.call_menu_pie", 'B', 'PRESS', shift=True)
    kmi.properties.name = EditBooleanPie.bl_idname
    addon_keymaps.append((kmm, kmi))

    kmi = kmm.keymap_items.new("wm.call_menu_pie", 'X', 'PRESS', shift=True)
    kmi.properties.name = DeletePie.bl_idname
    addon_keymaps.append((kmm, kmi))

    kmi = kmm.keymap_items.new("wm.call_menu_pie", 'V', 'PRESS', shift=True)
    kmi.properties.name = VertexPie.bl_idname
    addon_keymaps.append((kmm, kmi))

    kmi = kmm.keymap_items.new("wm.call_menu_pie", 'E', 'PRESS', shift=True)
    kmi.properties.name = EdgePie.bl_idname
    addon_keymaps.append((kmm, kmi))

    kmi = kmm.keymap_items.new("wm.call_menu_pie", 'F', 'PRESS', shift=True)
    kmi.properties.name = FacePie.bl_idname
    addon_keymaps.append((kmm, kmi))


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()
