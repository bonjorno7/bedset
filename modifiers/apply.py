import bpy


class Apply(bpy.types.Operator):
    """Apply modifiers on selected objects"""
    bl_options = {'REGISTER', 'UNDO'}
    bl_idname = "bedset.apply"
    bl_label = "Apply Modifiers"

    @classmethod
    def poll(cls, context):
        active = context.active_object

        if active is not None and active.mode == 'OBJECT':
            return len(context.selected_objects) > 0
            
        return False

    def duplicate(self, source):
        obj = source.copy()

        mesh = source.data.copy()
        obj.data = mesh

        col = source.users_collection[0]
        col.objects.link(obj)

        source.select_set(False)
        source.hide_set(True)

        return obj

    def execute(self, context):
        active = bpy.context.view_layer.objects.active

        for o in context.selected_objects:
            d = self.duplicate(o)

            if active is o:
                active = d

            bpy.context.view_layer.objects.active = d

            for m in d.modifiers:
                bpy.ops.object.modifier_apply(modifier=m.name)

        bpy.context.view_layer.objects.active = active

        return {'FINISHED'}
