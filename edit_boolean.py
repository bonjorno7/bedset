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

    def selected(self, geom):
        return [g for g in geom if g.select]

    def select(self, geom):
        for g in geom:
            g.select = True

    def unselected(self, geom):
        return [g for g in geom if not g.select]

    def unselect(self, geom):
        for g in geom:
            g.select = False

    def visible(self, geom):
        return [g for g in geom if not g.hide]

    def reveal(self, geom):
        for g in geom:
            g.hide = False

    def hidden(self, geom):
        return [g for g in geom if g.hide]

    def hide(self, geom):
        for g in geom:
            g.hide = True

    def execute(self, context):
        if self.kind in ['DIFFERENCE', 'UNION', 'INTERSECT']:
            bpy.ops.mesh.intersect_boolean(operation=self.kind)

        elif self.kind == 'SLICE':
            mesh = context.active_object.data
            bm = bmesh.from_edit_mesh(mesh)

            geometry = self.geometry(bm)
            visible = self.visible(geometry)
            hidden = self.hidden(geometry)

            target_one = self.unselected(visible)
            cutter_one = self.selected(visible)

            target_two = bmesh.ops.duplicate(bm, geom=target_one)["geom"]
            cutter_two = bmesh.ops.duplicate(bm, geom=cutter_one)["geom"]

            self.hide(target_two + cutter_two)
            bpy.ops.mesh.intersect_boolean(operation='DIFFERENCE')

            geometry = self.geometry(bm)
            self.hide(geometry)

            self.reveal(target_two + cutter_two)
            self.select(cutter_two)
            bpy.ops.mesh.intersect_boolean(operation='INTERSECT')

            geometry = self.geometry(bm)
            visible = self.visible(geometry)

            self.select(visible)
            self.reveal(geometry)
            self.hide(hidden)

            bm.normal_update()
            bmesh.update_edit_mesh(mesh)

        elif self.kind == 'CUT':
            mesh = context.active_object.data
            bm = bmesh.from_edit_mesh(mesh)

            bpy.ops.mesh.split()

            geometry = self.geometry(bm)
            cutter = self.selected(geometry)

            bpy.ops.mesh.intersect()

            geometry = self.geometry(bm)
            new = self.selected(geometry)

            self.unselect(geometry)
            self.select(cutter)

            bpy.ops.mesh.select_linked()

            cutter = self.selected(geometry)
            bmesh.ops.delete(bm, geom=cutter, context='VERTS')

            geometry = self.geometry(bm)
            self.select([g for g in new if g in geometry])

            bm.normal_update()
            bmesh.update_edit_mesh(mesh)

        return {'FINISHED'}
