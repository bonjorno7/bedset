import bpy
import bmesh
import math


class GetAngle(bpy.types.Operator):
    """Select edges based on angle"""
    bl_idname = "bedset.get_angle"
    bl_label = "Get Angle"
    bl_options = {'REGISTER', 'UNDO'}

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

    single_face: bpy.props.BoolProperty(
        name="Select Single Face Edges",
        description="Select edges with only one face attached to them",
        default=False,
    )

    @classmethod
    def poll(cls, context):
        active = context.active_object is not None
        edit = context.active_object.mode == "EDIT"
        return active and edit

    def select(self, e):
        a = e.calc_face_angle(None)

        if a is None:
            if self.single_face:
                e.select = True

        elif a > self.angle:
            e.select = True

    def execute(self, context):
        bpy.ops.mesh.select_mode(type='EDGE')
        mesh = context.active_object.data
        bm = bmesh.from_edit_mesh(mesh)
        selected = [e for e in bm.edges if e.select]

        if selected:
            for e in selected:
                for f in e.link_faces:
                    f.select = False

            for e in selected:
                self.select(e)

        else:
            for e in bm.edges:
                self.select(e)

        bmesh.update_edit_mesh(mesh)
        return {'FINISHED'}

    def draw(self, context):
        self.layout.prop(self, "angle")
        self.layout.prop(self, "single_face")
