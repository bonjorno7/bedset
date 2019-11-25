import bpy
import bmesh


class EditBoolean(bpy.types.Operator):
    """Perform boolean operation with selected on unselected"""
    bl_options = {'REGISTER', 'UNDO'}
    bl_idname = "bedset.edit_boolean"
    bl_label = "Edit Boolean"

    kind: bpy.props.EnumProperty(
        name="Kind",
        description="What kind of boolean operation to perform",
        items=(
            ('DIFFERENCE', "Difference", "Remove selected from unselected"),
            ('UNION', "Union", "Add selected to unselected"),
            ('INTERSECT', "Intersect", "Intersect selected with unselected"),
            ('SLICE', "Slice", "Extract selected from unselected"),
            ('CUT', "Cut", "Use selected as knife on unselected"),
        ),
    )

    @classmethod
    def poll(cls, context):
        active = context.active_object
        return active is not None and active.mode == 'EDIT'

    def geometry(self, bm):
        return bm.verts[:] + bm.edges[:] + bm.faces[:]

    def selected(self, bm):
        verts = [v for v in bm.verts if v.select]
        edges = [e for e in bm.edges if e.select]
        faces = [f for f in bm.faces if f.select]
        return verts + edges + faces

    def unselected(self, bm):
        verts = [v for v in bm.verts if not v.select]
        edges = [e for e in bm.edges if not e.select]
        faces = [f for f in bm.faces if not f.select]
        return verts + edges + faces

    def select(self, geom):
        for g in geom:
            g.select = True

    def unselect(self, geom):
        for g in geom:
            g.select = False

    def hidden(self, bm):
        verts = [v for v in bm.verts if v.hide]
        edges = [e for e in bm.edges if e.hide]
        faces = [f for f in bm.faces if f.hide]
        return verts + edges + faces

    def unhidden(self, bm):
        verts = [v for v in bm.verts if not v.hide]
        edges = [e for e in bm.edges if not e.hide]
        faces = [f for f in bm.faces if not f.hide]
        return verts + edges + faces

    def hide(self, geom):
        for g in geom:
            g.hide = True

    def unhide(self, geom):
        for g in geom:
            g.hide = False

    def execute(self, context):
        if self.kind in ['DIFFERENCE', 'UNION', 'INTERSECT']:
            bpy.ops.mesh.intersect_boolean(operation=self.kind)

        elif self.kind == 'SLICE':
            mesh = context.active_object.data
            bm = bmesh.from_edit_mesh(mesh)

            target_one = self.unselected(bm)
            cutter_one = self.selected(bm)

            target_two = bmesh.ops.duplicate(bm, geom=target_one)["geom"]
            cutter_two = bmesh.ops.duplicate(bm, geom=cutter_one)["geom"]

            self.hide(target_two + cutter_two)
            bpy.ops.mesh.intersect_boolean(operation='DIFFERENCE')

            self.hide(self.geometry(bm))
            self.unhide(target_two + cutter_two)
            self.select(cutter_two)
            bpy.ops.mesh.intersect_boolean(operation='INTERSECT')

            self.select(self.unhidden(bm))
            self.unhide(self.geometry(bm))
            bmesh.update_edit_mesh(mesh)

        elif self.kind == 'CUT':
            mesh = context.active_object.data
            bm = bmesh.from_edit_mesh(mesh)
            cutter = self.selected(bm)

            bpy.ops.mesh.intersect()
            new = self.selected(bm)
            self.unselect(new)
            self.select(cutter)

            bmesh.ops.delete(bm, geom=self.selected(bm), context='VERTS')
            self.select([g for g in new if g in self.geometry(bm)])
            bmesh.update_edit_mesh(mesh)

        return {'FINISHED'}
