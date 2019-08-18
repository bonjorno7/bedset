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
            ('EXTRACT', "Extract", "Extract selected from active"),
            ('INSET', "Inset", "Create an inset into active from selected"),
        ),
    )

    @classmethod
    def poll(cls, context):
        active = context.active_object
        if active is not None and active.mode == 'OBJECT':
            return len(context.selected_objects) > 1
        return False

    def duplicate(self, source, name):
        obj = source.copy()
        obj.name = source.name + name
        col = source.users_collection[0]
        col.objects.link(obj)
        obj.select_set(False)
        return obj

    def make_inset(self, source):
        obj = self.duplicate(source, "Inset")
        obj.display_type = 'WIRE'
        obj.hide_render = True
        return obj

    def make_extract(self, source):
        return self.duplicate(source, "Extract")

    def make_cutter(self, obj):
        obj.name = "Cutter " + obj.name
        obj.display_type = 'WIRE'
        obj.hide_render = True

    def execute(self, context):
        active = context.active_object
        cutters = [o for o in context.selected_objects if o is not active]

        if self.kind in ['DIFFERENCE', 'UNION', 'INTERSECT']:
            for cutter in cutters:
                self.make_cutter(cutter)
                boolean = active.modifiers.new(name="Boolean", type='BOOLEAN')
                boolean.operation = self.kind
                boolean.object = cutter
                boolean.show_expanded = False

        elif self.kind == 'INSET':
            for cutter in cutters:
                self.make_cutter(cutter)
                inset = self.make_inset(active)

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

        elif self.kind == 'EXTRACT':
            for cutter in cutters:
                self.make_cutter(cutter)
                extract = self.make_extract(active)

                intersect = extract.modifiers.new(name="Boolean", type='BOOLEAN')
                intersect.operation = 'INTERSECT'
                intersect.object = cutter
                intersect.show_expanded = False

                difference = active.modifiers.new(name="Boolean", type='BOOLEAN')
                difference.operation = 'DIFFERENCE'
                difference.object = cutter
                difference.show_expanded = False

        active.select_set(False)
        context.view_layer.objects.active = cutters[0]

        return {'FINISHED'}

    def draw(self, context):
        self.layout.prop(self, "kind")
