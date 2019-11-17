import bpy
import bmesh


class ModBoolean(bpy.types.Operator):
    """Add boolean modifiers with selected on active"""
    bl_options = {'REGISTER', 'UNDO'}
    bl_idname = "bedset.mod_boolean"
    bl_label = "Modifier Boolean"

    kind: bpy.props.EnumProperty(
        name="Kind",
        description="What kind of boolean operation to perform",
        items=(
            ('DIFFERENCE', "Difference", "Remove selected from active"),
            ('UNION', "Union", "Add selected to active"),
            ('INTERSECT', "Intersect", "Intersect selected with active"),
            ('SLASH', "Slash", "Separate selected from active"),
            ('INSET', "Inset", "Create an inset into active from selected"),
        ),
    )

    @classmethod
    def poll(cls, context):
        active = context.active_object
        if active is not None and active.mode == 'OBJECT':
            return len(context.selected_objects) > 1
        return False

    def execute(self, context):
        active = context.active_object
        cutters = [o for o in context.selected_objects if o is not active]

        if self.kind in ['DIFFERENCE', 'UNION', 'INTERSECT']:
            for cutter in cutters:
                cutter.display_type = 'WIRE'
                cutter.hide_render = True
                boolean = active.modifiers.new(name="Boolean", type='BOOLEAN')
                boolean.operation = self.kind
                boolean.object = cutter
                boolean.show_expanded = False

        elif self.kind == 'SLASH':
            for cutter in cutters:
                cutter.display_type = 'WIRE'
                cutter.hide_render = True

                extract = active.copy()
                collection = active.users_collection[0]
                collection.objects.link(extract)
                extract.select_set(False)

                intersect = extract.modifiers.new(name="Boolean", type='BOOLEAN')
                intersect.operation = 'INTERSECT'
                intersect.object = cutter
                intersect.show_expanded = False

                difference = active.modifiers.new(name="Boolean", type='BOOLEAN')
                difference.operation = 'DIFFERENCE'
                difference.object = cutter
                difference.show_expanded = False

        elif self.kind == 'INSET':
            for cutter in cutters:
                cutter.display_type = 'WIRE'
                cutter.hide_render = True

                inset = active.copy()
                collection = active.users_collection[0]
                collection.objects.link(inset)
                inset.select_set(False)
                inset.display_type = 'WIRE'
                inset.hide_render = True

                solidify = inset.modifiers.new(name="Solidify", type='SOLIDIFY')
                solidify.use_even_offset = True
                solidify.thickness = 0.1
                solidify.offset = 0.0
                solidify.show_expanded = True

                intersect = inset.modifiers.new(name="Boolean", type='BOOLEAN')
                intersect.operation = 'INTERSECT'
                intersect.object = cutter
                intersect.show_expanded = False

                difference = active.modifiers.new(name="Boolean", type='BOOLEAN')
                difference.operation = 'DIFFERENCE'
                difference.object = inset
                difference.show_expanded = False

        active.select_set(False)
        context.view_layer.objects.active = cutters[0]

        return {'FINISHED'}

    def draw(self, context):
        self.layout.prop(self, "kind")
