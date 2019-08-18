import bpy
import bmesh


class GetEdge(bpy.types.Operator):
    """Select edges based on Seam / Sharp / Bevel / Crease"""
    bl_options = {'REGISTER', 'UNDO'}
    bl_idname = "bedset.get_edge"
    bl_label = "Get Edge"

    kind: bpy.props.EnumProperty(
        name="Kind",
        description="What kind of edges to select",
        items=(
            ('SEAM', "Seam", "Select edges based on Seam"),
            ('SHARP', "Sharp", "Select edges based on Sharp"),
            ('BEVEL', "Bevel", "Select edges based on Bevel"),
            ('CREASE', "Crease", "Select edges based on Crease"),
            ('NOT_SEAM', "Not Seam", "Select edges based on Not Seam"),
            ('NOT_SHARP', "Not Sharp", "Select edges based on Not Sharp"),
            ('NOT_BEVEL', "Not Bevel", "Select edges based on Not Bevel"),
            ('NOT_CREASE', "Not Crease", "Select edges based on Not Crease"),
            ('NOT_ANY', "Not Any", "Select edges based on Not Any"),
        ),
    )

    @classmethod
    def poll(cls, context):
        active = context.active_object
        return active is not None and active.mode == 'EDIT'

    def execute(self, context):
        bpy.ops.mesh.select_mode(type='EDGE')
        mesh = context.active_object.data
        bm = bmesh.from_edit_mesh(mesh)

        selected = [e for e in bm.edges if e.select]
        selected = selected if selected else bm.edges

        for f in bm.faces:
            f.select = False

        bevel = bm.edges.layers.bevel_weight.verify()
        crease = bm.edges.layers.crease.verify()

        for e in selected:
            if self.kind == 'SEAM':
                e.select = e.seam

            elif self.kind == 'SHARP':
                e.select = not e.smooth

            elif self.kind == 'BEVEL':
                e.select = e[bevel]

            elif self.kind == 'CREASE':
                e.select = e[crease]

            elif self.kind == 'NOT_SEAM':
                e.select = not e.seam

            elif self.kind == 'NOT_SHARP':
                e.select = e.smooth

            elif self.kind == 'NOT_BEVEL':
                e.select = not e[bevel]

            elif self.kind == 'NOT_CREASE':
                e.select = not e[crease]

            elif self.kind == 'NOT_ANY':
                e.select = not e.seam and e.smooth and not e[bevel] and not e[crease]

        bmesh.update_edit_mesh(mesh)
        return {'FINISHED'}

    def draw(self, context):
        self.layout.prop(self, "kind")
