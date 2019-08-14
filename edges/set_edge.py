import bpy
import bmesh


class SetEdge(bpy.types.Operator):
    """Mark / Clear selected edges as Seam / Sharp / Bevel / Crease"""
    bl_idname = "bedset.set_edge"
    bl_label = "Set Edge"
    bl_options = {'REGISTER', 'UNDO'}

    kind: bpy.props.EnumProperty(
        name="Kind",
        description="What to mark the selected edges as",
        items=(
            ('MARK_SEAM', "Mark Seam", "Mark selected edges as Seam"),
            ('MARK_SHARP', "Mark Sharp", "Mark selected edges as Sharp"),
            ('MARK_BEVEL', "Mark Bevel", "Mark selected edges as Bevel"),
            ('MARK_CREASE', "Mark Crease", "Mark selected edges as Crease"),
            ('CLEAR_SEAM', "Clear Seam", "Clear Seam from selected edges"),
            ('CLEAR_SHARP', "Clear Sharp", "Clear Sharp from selected edges"),
            ('CLEAR_BEVEL', "Clear Bevel", "Clear Bevel from selected edges"),
            ('CLEAR_CREASE', "Clear Crease", "Clear Crease from selected edges"),
            ('CLEAR_ALL', "Clear All", "Clear All from selected edges"),
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

        bevel = bm.edges.layers.bevel_weight.verify()
        crease = bm.edges.layers.crease.verify()

        selected = [e for e in bm.edges if e.select]
        selected = selected if selected else bm.edges

        if self.kind == 'MARK_SEAM':
            for e in selected:
                e.seam = True

        if self.kind == 'MARK_SHARP':
            for e in selected:
                e.smooth = False

        if self.kind == "MARK_BEVEL":
            for e in selected:
                e[bevel] = 1

        if self.kind == "MARK_CREASE":
            for e in selected:
                e[crease] = 1

        if self.kind == 'CLEAR_SEAM':
            for e in selected:
                e.seam = False

        if self.kind == 'CLEAR_SHARP':
            for e in selected:
                e.smooth = True

        if self.kind == "CLEAR_BEVEL":
            for e in selected:
                e[bevel] = 0

        if self.kind == "CLEAR_CREASE":
            for e in selected:
                e[crease] = 0

        if self.kind == "CLEAR_ALL":
            for e in selected:
                e.seam = False
                e.smooth = True
                e[bevel] = 0
                e[crease] = 0

        bmesh.update_edit_mesh(mesh)
        return {'FINISHED'}

    def draw(self, context):
        self.layout.prop(self, "kind")
