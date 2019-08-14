import bpy


class ApplyBoolean(bpy.types.Operator):
    """Apply boolean modifiers on selected objects"""
    bl_idname = "bedset.apply_boolean"
    bl_label = "Apply Boolean"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        active = context.active_object
        if active is not None and active.mode == 'OBJECT':
            return len(context.selected_objects) > 0
        return False

    def execute(self, context):
        active = context.active_object

        for o in context.selected_objects:
            bpy.context.view_layer.objects.active = o
            for m in o.modifiers:
                if m.type == 'BOOLEAN':
                    bpy.ops.object.modifier_apply(modifier=m.name)

        bpy.context.view_layer.objects.active = active
        return {'FINISHED'}

    def draw(self, context):
        self.layout.prop(self, "kind")
