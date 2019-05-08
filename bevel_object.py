import bpy


class BevelObject(bpy.types.Operator):
    """Add a weighted bevel modifier to the active object"""
    bl_idname = "bedset.bevel_object"
    bl_label = "Bevel Object"
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
        subtype='DISTANCE',
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        active = context.active_object
        bevel = active.modifiers.new(name="Bevel", type='BEVEL')

        bevel.width = self.width
        bevel.segments = self.segments

        bevel.limit_method = 'WEIGHT'
        return {'FINISHED'}

    def draw(self, context):
        self.layout.prop(self, "width")
        self.layout.prop(self, "segments")
