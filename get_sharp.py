import os, subprocess, math
import bpy, bmesh, mathutils


class HARD_OT_GetSharp(bpy.types.Operator):
    """Select edges based on angle, can Mark Sharp / Bevel Weight / Crease"""
    bl_idname = "hard.get_sharp"
    bl_label = "Get Sharp"
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

    sharp: bpy.props.BoolProperty(
        name="Sharp",
        description="Mark edges as sharp",
        default=False,
    )

    bevel: bpy.props.BoolProperty(
        name="Bevel",
        description="Set bevel weight",
        default=False,
    )

    crease: bpy.props.BoolProperty(
        name="Crease",
        description="Crease edges",
        default=False,
    )

    seam: bpy.props.BoolProperty(
        name="Seam",
        description="Mark edges as seam",
        default=False,
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.mode == "EDIT"

    def edge_sharp(self, e):
        a = e.calc_face_angle(None)
        if a is not None and a > self.angle:
            e.select = True
            e.smooth = False if self.sharp else True
            # e.bevel_weight = 1.0 if self.bevel else 0.0
            # e.crease = 1.0 if self.crease else 0.0
            e.seam = True if self.seam else False

    def execute(self, context):
        bpy.ops.mesh.select_mode(type='EDGE')
        mesh = context.active_object.data
        bm = bmesh.from_edit_mesh(mesh)

        edge_sel = [e for e in bm.edges if e.select]

        if edge_sel:
            for e in edge_sel:
                for f in e.link_faces:
                    f.select = False

        if edge_sel and len(edge_sel) < len(bm.edges[:]):
            for e in edge_sel:
                self.edge_sharp(e)
        else:
            for e in bm.edges:
                self.edge_sharp(e)

        bmesh.update_edit_mesh(mesh)
        return {'FINISHED'}

    def draw(self, context):
        self.layout.prop(self, "angle")

        flow = self.layout.grid_flow()

        col = flow.column()
        col.prop(self, "sharp")

        col = flow.column()
        col.prop(self, "bevel")

        col = flow.column()
        col.prop(self, "crease")

        col = flow.column()
        col.prop(self, "seam")
