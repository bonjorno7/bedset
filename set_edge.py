import bpy
import bmesh


class SetEdge(bpy.types.Operator):
    """Mark / Clear selected edges as Seam / Sharp / Bevel / Crease"""
    bl_idname = "bedset.set_edge"
    bl_label = "Set Edge"
    bl_options = {'REGISTER', 'UNDO'}

    kind: bpy.props.EnumProperty(
        name = "Kind",
        description = "What to mark the selected edges as",
        items=(
            ('MARK_SEAM', "Mark Seam", "Mark selected edges as Seam"),
            ('MARK_SHARP', "Mark Sharp", "Mark selected edges as Sharp"),
            ('MARK_BEVEL', "Mark Bevel", "Mark selected edges as Bevel"),
            ('MARK_CREASE', "Mark Crease", "Mark selected edges as Crease"),
            ('CLEAR_SEAM', "Clear Seam", "Clear Seam from selected edges"),
            ('CLEAR_SHARP', "Clear Sharp", "Clear Sharp from selected edges"),
            ('CLEAR_BEVEL', "Clear Bevel", "Clear Bevel from selected edges"),
            ('CLEAR_CREASE', "Clear Crease", "Clear Crease from selected edges"),
        ),
    )

    @classmethod
    def poll(cls, context):
        active = context.active_object is not None
        edit = context.active_object.mode == "EDIT"
        return active and edit

    def execute(self, context):
        mesh = context.active_object.data
        bm = bmesh.from_edit_mesh(mesh)

        bevel_layer = bm.edges.layers.bevel_weight.verify()
        crease_layer = bm.edges.layers.crease.verify()

        for e in bm.edges:
            if e.select:
                if self.kind == 'MARK_SEAM':
                    e.seam = True

                if self.kind == 'MARK_SHARP':
                    e.smooth = False

                if self.kind == "MARK_BEVEL":
                    e[bevel_layer] = 1

                if self.kind == "MARK_CREASE":
                    e[crease_layer] = 1

                if self.kind == 'CLEAR_SEAM':
                    e.seam = False

                if self.kind == 'CLEAR_SHARP':
                    e.smooth = True

                if self.kind == "CLEAR_BEVEL":
                    e[bevel_layer] = 0

                if self.kind == "CLEAR_CREASE":
                    e[crease_layer] = 0

        return {'FINISHED'}

    def draw(self, context):
        self.layout.prop(self, "kind")
