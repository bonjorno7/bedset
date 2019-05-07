import bpy
from . get_sharp import GetSharp
from . get_edge import GetEdge
from . set_edge import SetEdge
from . edge_menu import EdgeMenu
from . boolean import Boolean
from . boolean_menu import BooleanMenu


bl_info = {
    "blender": (2, 80, 0),
    "name": "BedSet",
    "description": "Some tools to make Blender more comfortable",
    "author": "bonjorno7",
    "version": (0, 0, 4),
    "location": "3D View > Sidebar",
    "category": "Mesh",
    "warning": "",
}


classes = (
    GetSharp,
    GetEdge,
    SetEdge,
    EdgeMenu,
    Boolean,
    BooleanMenu,
)


addon_keymaps = []


def register():
    for c in classes:
        bpy.utils.register_class(c)

    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')

    kmi_mnu = km.keymap_items.new("wm.call_menu", "Q", "PRESS", ctrl=True)
    kmi_mnu.properties.name = BooleanMenu.bl_idname
    addon_keymaps.append((km, kmi_mnu))

    kmi_mnu = km.keymap_items.new("wm.call_menu", "E", "PRESS", shift=True)
    kmi_mnu.properties.name = EdgeMenu.bl_idname
    addon_keymaps.append((km, kmi_mnu))


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()


if __name__ == "__main__":
    register()
