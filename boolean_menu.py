import bpy
from . boolean import Boolean


class BooleanMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_BooleanMenu"
    bl_label = "Boolean Stuff"

    @classmethod
    def poll(cls, context):
        active = context.active_object is not None
        edit = context.active_object.mode == "EDIT"
        return active and edit

    def draw(self, context):
        self.layout.operator(Boolean.bl_idname)
