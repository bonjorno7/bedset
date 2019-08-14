import bpy


class Solidify(bpy.types.Operator):
    """Add solidify modifiers to the selected objects"""
    bl_idname = "bedset.modifier_solidify"
    bl_label = "(Y) Solidify"
    bl_icon = 'MOD_SOLIDIFY'
    bl_options = {'REGISTER', 'UNDO'}

    thickness: bpy.props.FloatProperty(
        name="Thickness",
        description="Thickness of the shell",
        default=0.1,
        min=0,
        max=1000000,
        soft_min=0,
        soft_max=1000,
        step=1,
        precision=3,
        subtype='DISTANCE',
    )

    offset: bpy.props.FloatProperty(
        name="Offset",
        description="Offset the thickness from the center",
        default=-1,
        min=-1,
        max=1,
        step=1,
        precision=3,
        subtype='FACTOR',
    )

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0

    def execute(self, context):
        for o in context.selected_objects:
            mod = None

            for m in o.modifiers:
                if m.type == 'SOLIDIFY':
                    mod = m
                    break

            if not mod:
                mod = o.modifiers.new(name='Solidify', type='SOLIDIFY')

            mod.thickness = self.thickness
            mod.offset = self.offset
            mod.use_even_offset = True

        return {'FINISHED'}

    def draw(self, context):
        self.layout.prop(self, "thickness")
        self.layout.prop(self, "offset")
