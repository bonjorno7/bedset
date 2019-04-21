import bpy

from . import get_sharp

bl_info = {
    "blender": (2, 80, 0),
    "name": "Hard",
    "description": "Some Tools",
    "author": "bonjorno7",
    "version": (0, 0, 1),
    "location": "3D View > Sidebar",
    "category": "Mesh",
    "warning": "",
}

classes = (
    get_sharp.HARD_OT_GetSharp,
)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
