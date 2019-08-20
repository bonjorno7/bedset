import bpy


class ApplyModifiers(bpy.types.Operator):
    """Apply modifiers on selected objects"""
    bl_options = {'REGISTER', 'UNDO'}
    bl_idname = "bedset.apply_modifiers"
    bl_label = "Apply Modifiers"

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0

    def execute(self, context):
        selected = context.selected_objects

        bpy.ops.object.convert(target='MESH', keep_original=True)

        for obj in selected:
            obj.hide_set(True)

        return {'FINISHED'}
