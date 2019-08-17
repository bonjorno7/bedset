import bpy


class Bevel(bpy.types.Operator):
    bl_options = {"REGISTER", "UNDO", "GRAB_CURSOR", "BLOCKING"}
    bl_idname = "bedset.bevel"
    bl_label = "(B) Bevel"
    bl_icon = 'MOD_BEVEL'

    @classmethod
    def poll(cls, context):
        return context.object is not None

    prop_width: bpy.props.FloatProperty(
        name="Width", subtype='DISTANCE',
        description="Width of the bevel",
        default=0.1, min=0, max=1000000,
        step=1, precision=3)

    prop_segments: bpy.props.IntProperty(
        name="Segments", subtype='UNSIGNED',
        description="Number of segments",
        default=1, min=1, max=100, step=1)

    def get_mod(self, context):
        self.mod = None

        for m in context.object.modifiers:
            if m.type == 'BEVEL':
                self.mod = m
                break

        if not self.mod:
            self.new = True
            self.mod = context.object.modifiers.new(name="Bevel", type='BEVEL')
            self.mod.limit_method = 'ANGLE'
            self.mod.width = self.prop_width
            self.mod.segments = self.prop_segments

    def invoke(self, context, event):
        self.new = False
        self.get_mod(context)

        self.width = self.mod.width
        self.segments = self.mod.segments

        self.prop_width = self.width
        self.prop_segments = self.segments

        self.init_width = self.width
        self.init_segments = self.segments

        self.prev_mouse_x = event.mouse_x

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        self.get_mod(context)
        self.mod.width = self.prop_width
        self.mod.segments = self.prop_segments
        return {'FINISHED'}

    def modal(self, context, event):
        if event.type in {'LEFTMOUSE', 'ENTER', 'SPACE'}:
            return {'FINISHED'}

        if event.type == 'A':
            bpy.ops.object.modifier_apply(modifier=self.mod.name)
            return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            if self.new:
                context.object.modifiers.remove(self.mod)

            else:
                self.mod.width = self.init_width
                self.mod.segments = self.init_segments

            return {'CANCELLED'}

        elif event.type == 'WHEELUPMOUSE':
            self.segments += 1

            if self.segments > 100:
                self.segments = 100

            self.prop_segments = self.segments

        elif event.type == 'WHEELDOWNMOUSE':
            self.segments -= 1

            if self.segments < 1:
                self.segments = 1

            self.prop_segments = self.segments

        elif event.type == 'MOUSEMOVE':
            delta = (event.mouse_x - self.prev_mouse_x) / 500

            if event.shift:
                delta /= 10

            self.width += delta

            if self.width < 0:
                self.width = 0

            self.prop_width = self.width

            self.prev_mouse_x = event.mouse_x

        if event.ctrl:
            self.prop_width = round(self.width, 2 if event.shift else 1)
        else:
            self.prop_width = self.width

        self.execute(context)

        return {'RUNNING_MODAL'}

    def draw(self, context):
        self.layout.prop(self, "prop_width")
        self.layout.prop(self, "prop_segments")
