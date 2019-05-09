import bpy


class ObjectBoolean(bpy.types.Operator):
    """Add boolean modifiers with selected on active"""
    bl_idname = "bedset.object_boolean"
    bl_label = "Object Boolean"
    bl_options = {'REGISTER', 'UNDO'}

    kind: bpy.props.EnumProperty(
        name="Kind",
        description="What kind of boolean operation to perform",
        items=(
            ('DIFFERENCE', "Difference", "Remove selected from active"),
            ('UNION', "Union", "Add selected to active"),
            ('INTERSECT', "Intersect", "Intersect selected with active"),
        ),
    )

    @classmethod
    def poll(cls, context):
        active = context.active_object
        if active is not None and active.mode == 'OBJECT':
            return len(context.selected_objects) > 1
        return False

    def execute(self, context):
        active = context.active_object

        for o in context.selected_objects:
            if not o is active:
                boolean = active.modifiers.new(
                    name="Bedset Boolean", type='BOOLEAN')
                boolean.operation = self.kind
                boolean.object = o
                o.display_type = 'WIRE'

        return {'FINISHED'}

    def draw(self, context):
        self.layout.prop(self, "kind")
