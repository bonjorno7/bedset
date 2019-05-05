import bpy
from . get_sharp import GetSharp
from . get_edge import GetEdge
from . set_edge import SetEdge


bl_info = {
    "blender": (2, 80, 0),
    "name": "BedSet",
    "description": "Some tools to make Blender more comfortable",
    "author": "bonjorno7",
    "version": (0, 0, 3),
    "location": "3D View > Sidebar",
    "category": "Mesh",
    "warning": "",
}


classes = (
    GetSharp,
    GetEdge,
    SetEdge,
)


register, unregister = bpy.utils.register_classes_factory(classes)


if __name__ == "__main__":
    register()
