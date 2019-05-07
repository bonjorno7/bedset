import bpy
import bmesh


class Boolean(bpy.types.Operator):
    """Perform boolean operation with selected on unselected"""
    bl_idname = "bedset.boolean"
    bl_label = "Boolean"
    bl_options = {'REGISTER', 'UNDO'}

    kind: bpy.props.EnumProperty(
        name="Kind",
        description="What kind of boolean operation to perform",
        items=(
            ('DIFFERENCE', "Difference", "Remove selected from unselected"),
            ('UNION', "Union", "Add selected to unselected"),
            ('INTERSECT', "Intersect", "Intersect selected with unselected"),
            ('CUT', "Cut", "Use selected as knife on unselected"),
        ),
    )

    @classmethod
    def poll(cls, context):
        active = context.active_object is not None
        edit = context.active_object.mode == "EDIT"
        return active and edit

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

    def execute(self, context):
        if self.kind == 'DIFFERENCE':
            bpy.ops.mesh.intersect_boolean(operation='DIFFERENCE')

        if self.kind == 'UNION':
            bpy.ops.mesh.intersect_boolean(operation='UNION')

        if self.kind == 'INTERSECT':
            bpy.ops.mesh.intersect_boolean(operation='INTERSECT')

        if self.kind == 'CUT':
            mesh = context.active_object.data
            bm = bmesh.from_edit_mesh(mesh)
            cutter = self.selected(bm)
            target = self.unselected(bm)

            bpy.ops.mesh.intersect()
            selected = self.selected(bm)
            for g in selected:
                g.select = False

            for g in cutter:
                g.select = True
            bmesh.update_edit_mesh(mesh)
            bpy.ops.mesh.select_linked()

            delete = self.selected(bm)
            bmesh.ops.delete(bm, geom=delete, context='VERTS')
            bmesh.update_edit_mesh(mesh)

            unselected = self.unselected(bm)
            for g in selected:
                if g in unselected:
                    g.select = True
            bmesh.update_edit_mesh(mesh)

        return {'FINISHED'}
