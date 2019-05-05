import bpy
import bmesh


class Boolean(bpy.types.Operator):
    """Perform boolean operation with selected on unselected"""
    bl_idname = "bedset.boolean"
    bl_label = "Boolean"
    bl_options = {'REGISTER', 'UNDO'}

    kind: bpy.props.EnumProperty(
        name="Kind",
        description="What kind of boolean operation to perform",
        items=(
            ('DIFFERENCE', "Difference", "Remove selected from unselected"),
            ('UNION', "Union", "Add selected to unselected"),
            ('INTERSECT', "Intersect", "Intersect selected with unselected"),
            ('CUT', "Cut", "Use selected as knife on unselected"),
        ),
    )

    @classmethod
    def poll(cls, context):
        active = context.active_object is not None
        edit = context.active_object.mode == "EDIT"
        return active and edit

    def execute(self, context):
        if self.kind == 'CUT':
            bpy.ops.mesh.intersect()
