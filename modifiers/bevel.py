import bpy


class Bevel(bpy.types.Operator):
    """Add weighted bevel modifiers to the selected objects"""
    bl_idname = "bedset.modifier_bevel"
    bl_label = "(B) Bevel"
    bl_icon = 'MOD_BEVEL'
    bl_options = {'REGISTER', 'UNDO'}

    width: bpy.props.FloatProperty(
        name="Width",
        description="Width of the bevel",
        default=0.1,
        min=0,
        max=1000000,
        soft_min=0,
        soft_max=1000,
        step=1,
        precision=3,
        subtype='DISTANCE',
    )

    segments: bpy.props.IntProperty(
        name="Segments",
        description="Number of segments",
        default=4,
        min=1,
        max=1024,
        soft_min=1,
        soft_max=64,
        step=1,
        subtype='UNSIGNED',
    )

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0

    def execute(self, context):
        for o in context.selected_objects:
            mod = None

            for m in o.modifiers:
                if m.type == 'BEVEL':
                    mod = m
                    break

            if not mod:
                mod = o.modifiers.new(name='Bevel', type='BEVEL')

            mod.width = self.width
            mod.segments = self.segments
            mod.limit_method = 'WEIGHT'

        return {'FINISHED'}

    def draw(self, context):
        self.layout.prop(self, "width")
        self.layout.prop(self, "segments")
