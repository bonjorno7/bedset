import bpy
import bmesh


class GetEdge(bpy.types.Operator):
    """Select edges based on Seam / Sharp / Bevel / Crease"""
    bl_idname = "bedset.get_edge"
    bl_label = "Get Edge"
    bl_options = {'REGISTER', 'UNDO'}

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
        active = context.active_object is not None
        edit = context.active_object.mode == "EDIT"
        return active and edit

    def select(self, e, bevel_layer, crease_layer):
        if self.kind == 'SEAM' and e.seam:
            e.select = True

        if self.kind == 'SHARP' and not e.smooth:
            e.select = True

        if self.kind == 'BEVEL' and e[bevel_layer]:
            e.select = True

        if self.kind == 'CREASE' and e[crease_layer]:
            e.select = True

        if self.kind == 'NOT_SEAM' and not e.seam:
            e.select = True

        if self.kind == 'NOT_SHARP' and e.smooth:
            e.select = True

        if self.kind == 'NOT_BEVEL' and not e[bevel_layer]:
            e.select = True

        if self.kind == 'NOT_CREASE' and not e[crease_layer]:
            e.select = True

        if (
            self.kind == 'NOT_ANY'
            and not e.seam
            and e.smooth
            and not e[bevel_layer]
            and not e[crease_layer]
        ):
            e.select = True

    def execute(self, context):
        bpy.ops.mesh.select_mode(type='EDGE')
        mesh = context.active_object.data
        bm = bmesh.from_edit_mesh(mesh)
        selected = [e for e in bm.edges if e.select]

        if bm.edges.layers.bevel_weight:
            bevel_layer = bm.edges.layers.bevel_weight.active
        else:
            bevel_layer = None

        if bm.edges.layers.crease:
            crease_layer = bm.edges.layers.crease.active
        else:
            crease_layer = None

        if selected:
            for e in selected:
                for f in e.link_faces:
                    f.select = False

            for e in selected:
                self.select(e, bevel_layer, crease_layer)

        else:
            for e in bm.edges:
                self.select(e, bevel_layer, crease_layer)

        bmesh.update_edit_mesh(mesh)
        return {'FINISHED'}

    def draw(self, context):
        self.layout.prop(self, "kind")
