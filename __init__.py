import bpy
from . get_sharp import GetSharp


bl_info = {
    "blender": (2, 80, 0),
    "name": "BedSet",
    "description": "Some tools to make Blender more comfortable",
    "author": "bonjorno7",
    "version": (0, 0, 2),
    "location": "3D View > Sidebar",
    "category": "Mesh",
    "warning": "",
}


classes = (
    GetSharp,
)


register, unregister = bpy.utils.register_classes_factory(classes)


if __name__ == "__main__":
    register()
