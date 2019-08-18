import bpy
import bmesh


# TODO: Some options for where to move it, instead of just to the 3D cursor


class MoveOrigin(bpy.types.Operator):
    """Move origins of the selected objects"""
    bl_options = {'REGISTER', 'UNDO'}
    bl_idname = "bedset.move_origin"
    bl_label = "Move Origin"

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0

    def execute(self, context):
        cursor = context.scene.cursor.location
        active = context.active_object

        for o in context.selected_objects:
            if o.data.is_editmode:
                bm = bmesh.from_edit_mesh(o.data)
            else:
                bm = bmesh.new()
                bm.from_mesh(o.data)

            move = o.location - cursor

            for vert in bm.verts:
                vert.co += move

            o.location = cursor

            if o.data.is_editmode:
                bmesh.update_edit_mesh(o.data)
            else:
                bm.to_mesh(o.data)
                o.data.update()

        bpy.context.view_layer.objects.active = active
        return {'FINISHED'}
