import bpy


class Solidify(bpy.types.Operator):
    bl_options = {"REGISTER", "UNDO", "GRAB_CURSOR", "BLOCKING"}
    bl_idname = "bedset.solidify"
    bl_label = "(Y) Solidify"
    bl_icon = 'MOD_SOLIDIFY'

    @classmethod
    def poll(cls, context):
        return context.object is not None

    prop_thickness: bpy.props.FloatProperty(
        name="Thickness", subtype='DISTANCE',
        description="Thickness of the shell",
        default=0.1, min=0, max=1000000,
        step=1, precision=3)

    prop_offset: bpy.props.FloatProperty(
        name="Offset", subtype='FACTOR',
        description="Offset the thickness from the center",
        default=-1, min=-1, max=1,
        step=1, precision=3)

    def get_mod(self, context):
        self.mod = None

        for m in context.object.modifiers:
            if m.type == 'SOLIDIFY':
                self.mod = m
                break

        if not self.mod:
            self.new = True
            self.mod = context.object.modifiers.new(name="Solidify", type='SOLIDIFY')
            self.mod.use_even_offset = True
            self.mod.thickness = self.prop_thickness
            self.mod.offset = self.prop_offset

    def invoke(self, context, event):
        self.new = False
        self.get_mod(context)

        self.thickness = self.mod.thickness
        self.offset = self.mod.offset

        self.prop_thickness = self.thickness
        self.prop_offset = self.offset

        self.init_thickness = self.thickness
        self.init_offset = self.offset

        self.prev_mouse_x = event.mouse_x

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        self.get_mod(context)
        self.mod.thickness = self.prop_thickness
        self.mod.offset = self.prop_offset
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
                self.mod.thickness = self.init_thickness
                self.mod.offset = self.init_offset

            return {'CANCELLED'}

        elif event.type == 'WHEELUPMOUSE':
            self.offset += 1

            if self.offset > 1:
                self.offset = 1

            self.prop_offset = self.offset

        elif event.type == 'WHEELDOWNMOUSE':
            self.offset -= 1

            if self.offset < -1:
                self.offset = -1

            self.prop_offset = self.offset

        elif event.type == 'MOUSEMOVE':
            delta = (event.mouse_x - self.prev_mouse_x) / 500

            if event.shift:
                delta /= 10

            self.thickness += delta

            if self.thickness < 0:
                self.thickness = 0

            self.prop_thickness = self.thickness

            self.prev_mouse_x = event.mouse_x

        if event.ctrl:
            self.prop_thickness = round(self.thickness, 2 if event.shift else 1)
        else:
            self.prop_thickness = self.thickness

        self.execute(context)

        return {'RUNNING_MODAL'}

    def draw(self, context):
        self.layout.prop(self, "prop_thickness")
        self.layout.prop(self, "prop_offset")
