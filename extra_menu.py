import bpy
from . autosmooth import AutoSmooth
from . bevel_object import BevelObject


class ExtraMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_ExtraMenu"
    bl_label = "Extra"

    def draw(self, context):
        self.layout.operator(AutoSmooth.bl_idname)
        self.layout.operator(BevelObject.bl_idname)
