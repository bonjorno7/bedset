import bpy
from . get_sharp import GetSharp
from . get_edge import GetEdge
from . set_edge import SetEdge


class EdgeMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_EdgeMenu"
    bl_label = "Edge Stuff"

    @classmethod
    def poll(cls, context):
        active = context.active_object is not None
        edit = context.active_object.mode == "EDIT"
        return active and edit

    def draw(self, context):
        self.layout.operator(GetSharp.bl_idname)
        self.layout.operator(GetEdge.bl_idname)
        self.layout.operator(SetEdge.bl_idname)
