import bpy
from . object_boolean import ObjectBoolean


class ObjectBooleanMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_ObjectBooleanMenu"
    bl_label = "Boolean"

    def draw(self, context):
        self.layout.operator(
            ObjectBoolean.bl_idname,
            text="Difference",
        ).kind = 'DIFFERENCE'

        self.layout.operator(
            ObjectBoolean.bl_idname,
            text="Union",
        ).kind = 'UNION'

        self.layout.operator(
            ObjectBoolean.bl_idname,
            text="Intersect",
        ).kind = 'INTERSECT'

        self.layout.operator(
            ObjectBoolean.bl_idname,
            text="Apply",
        ).kind = 'APPLY'
