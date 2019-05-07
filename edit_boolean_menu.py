import bpy
from . edit_boolean import EditBoolean


class EditBooleanMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_BooleanMenu"
    bl_label = "Boolean"

    def draw(self, context):
        self.layout.operator(
            EditBoolean.bl_idname,
            text="Difference",
        ).kind = 'DIFFERENCE'

        self.layout.operator(
            EditBoolean.bl_idname,
            text="Union",
        ).kind = 'UNION'

        self.layout.operator(
            EditBoolean.bl_idname,
            text="Intersect",
        ).kind = 'INTERSECT'

        self.layout.operator(
            EditBoolean.bl_idname,
            text="Cut",
        ).kind = 'CUT'
