import bpy
import bmesh
import math


class AutoSmooth(bpy.types.Operator):
    """Turn on autosmooth for this mesh"""
    bl_idname = "bedset.autosmooth"
    bl_label = "Auto Smooth"
    bl_options = {'REGISTER', 'UNDO'}

    smooth: bpy.props.BoolProperty(
        name="Use Auto Smooth",
        description="Toggle auto smooth on or off",
        default=True,
    )

    angle: bpy.props.FloatProperty(
        name="Angle",
        description="Angle above which to select edges",
        default=math.radians(30),
        min=0,
        max=math.radians(180),
        step=10,
        precision=3,
        subtype='ANGLE',
    )

    clear: bpy.props.BoolProperty(
        name="Clear Custom Split Normals Data",
        description="Remove the custom split normals layer, if it exists",
        default=False,
    )

    def execute(self, context):
        mesh = context.active_object.data
        mesh.use_auto_smooth = self.smooth
        mesh.auto_smooth_angle = self.angle

        if mesh.is_editmode:
            bm = bmesh.from_edit_mesh(mesh)
        else:
            bm = bmesh.new()
            bm.from_mesh(mesh)

        for f in bm.faces:
            f.smooth = self.smooth

        if mesh.is_editmode:
            bmesh.update_edit_mesh(mesh)
        else:
            bm.to_mesh(mesh)
            mesh.update()

        if self.clear and mesh.has_custom_normals:
            bpy.ops.mesh.customdata_custom_splitnormals_clear()
        return {'FINISHED'}

    def draw(self, context):
        self.layout.prop(self, "smooth")
        self.layout.prop(self, "angle")
        self.layout.prop(self, "clear")
