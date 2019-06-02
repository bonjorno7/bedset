import bpy
import os


class BakeSettings(bpy.types.PropertyGroup):
    """Settings for baking"""
    bl_idname = "BEDSET_PG_BakeSettings"

    def is_mesh(self, obj):
        return obj.type == 'MESH'

    cage: bpy.props.PointerProperty(
        name="Cage",
        description="Custom cage object for this bake (if not set, extrusion is used)",
        type=bpy.types.Object,
        poll=is_mesh,
    )

    resolutions = [
        ('64', "64", "64"),
        ('128', "128", "128"),
        ('256', "256", "256"),
        ('512', "512", "512"),
        ('1024', "1024", "1024"),
        ('2048', "2048", "2048"),
        ('4096', "4096", "4096"),
        ('8192', "8192", "8192"),
    ]

    width: bpy.props.EnumProperty(
        name="Width",
        description="Width of the textures",
        items=resolutions,
        default='1024'
    )

    height: bpy.props.EnumProperty(
        name="Height",
        description="Height of the textures",
        items=resolutions,
        default='1024'
    )

    margin: bpy.props.IntProperty(
        name="Margin",
        description="Margin to extend the edges of the bake by",
        default=16,
        soft_min=0,
        soft_max=64
    )


class Bake(bpy.types.Operator):
    """Bake the textures"""
    bl_idname = "bedset.bake"
    bl_label = "Bake PBR"
    bl_options = {'REGISTER'}

    def verify_folder(self, path):
        if not os.path.exists(path):
            os.mkdir(path)

        return path

    def verify_material(self, obj):
        mat = obj.active_material

        if not mat:
            mat = bpy.data.materials.new(name=obj.name)

            if obj.data.materials:
                obj.data.materials[0] = mat
            else:
                obj.data.materials.append(mat)

        return mat

    def verify_image(self, settings, path, name):
        img = None

        for i in bpy.data.images:
            if i.name == name:
                img = i

        if img:
            img.source = 'GENERATED'
            img.generated_width = int(settings.width)
            img.generated_height = int(settings.height)

        else:
            img = bpy.data.images.new(
                name=name, height=int(settings.height),
                alpha=False, width=int(settings.width)
            )

        if img.name[-1] in "de":
            img.colorspace_settings.name = 'sRGB'
        if img.name[-1] in "nrm":
            img.colorspace_settings.name = 'Non-Color'

        img.filepath = os.path.join(path, name + ".png")

        return img

    def save_image(self, context, img):
        image_settings = context.scene.render.image_settings
        file_format = image_settings.file_format
        color_depth = image_settings.color_depth
        compression = image_settings.compression
        color_mode = image_settings.color_mode

        image_settings.compression = 100
        image_settings.file_format = 'PNG'
        image_settings.color_depth = '16'

        if img.name[-1] in "dne":
            image_settings.color_mode = 'RGB'
        if img.name[-1] in "rm":
            image_settings.color_mode = 'BW'

        img.save_render(img.filepath)
        img.source = 'FILE'
        img.reload()

        image_settings.compression = compression
        image_settings.file_format = file_format
        image_settings.color_depth = color_depth
        image_settings.color_mode = color_mode

    def bake(self, settings, bake_type):
        bpy.ops.object.bake(
            type=bake_type, normal_space='TANGENT',
            normal_r='POS_X', normal_g='POS_Y', normal_b='POS_Z',
            width=int(settings.width), height=int(settings.height),
            margin=settings.margin, use_clear=True,
            use_selected_to_active=True, use_cage=True,
            cage_object=settings.cage.name, cage_extrusion=0
        )

    def clear_node_tree(self, node_tree):
        node_tree.nodes.clear()
        node_tree.links.clear()
        return node_tree

    def output_node(self, nodes, x, y):
        node = nodes.new("ShaderNodeOutputMaterial")
        node.location = [x, y]
        node.select = False
        return node

    def principled_node(self, nodes, x, y):
        node = nodes.new("ShaderNodeBsdfPrincipled")
        node.location = [x, y]
        node.select = False
        return node

    def normal_map_node(self, nodes, x, y):
        node = nodes.new("ShaderNodeNormalMap")
        node.location = [x, y]
        node.select = False
        node.hide = True
        return node

    def image_node(self, nodes, image, x, y):
        node = nodes.new("ShaderNodeTexImage")
        node.location = [x, y]
        node.select = False
        node.image = image
        node.hide = True
        return node

    def socket(self, node, identifier):
        for socket in node.outputs:
            if socket.identifier == identifier:
                return socket

        for socket in node.inputs:
            if socket.identifier == identifier:
                return socket

    def get_nodes(self, objs):
        nodes = []

        for o in objs:
            materials = [ms.material for ms in o.material_slots if ms.material]

            if not materials:
                self.report({'ERROR'}, o.name + " doesn't have any materials")
                return False

            for m in materials:
                principled_node = None
                output_node = None
                original_emission = None

                for n in m.node_tree.nodes:
                    if n.bl_idname == "ShaderNodeBsdfPrincipled":
                        principled_node = n

                        socket_emission = self.socket(principled_node, "Emission")
                        if socket_emission.links:
                            original_emission = socket_emission.links[0].from_socket

                    if n.bl_idname == "ShaderNodeOutputMaterial":
                        output_node = n

                if not principled_node:
                    self.report({'ERROR'}, m.name + " doesn't have a principled bsdf")
                    return False

                if not output_node:
                    self.report({'ERROR'}, m.name + " doesn't have an output node")
                    return False

                nodes.append([m.node_tree, principled_node, output_node, original_emission])

        return nodes

    @classmethod
    def poll(cls, context):
        if bpy.data.is_saved:
            if len(context.selected_objects) < 2:
                return False
            if context.scene.BedsetBakeSettings.cage:
                return True
        return False

    def execute(self, context):
        settings = context.scene.BedsetBakeSettings
        path = self.verify_folder(bpy.path.abspath("//PBR"))
        active = context.view_layer.objects.active

        selected = [o for o in context.view_layer.objects.selected if o is not active]
        selected_nodes = self.get_nodes(selected)
        if not selected_nodes:
            return {'FINISHED'}

        material = self.verify_material(active)
        node_tree = self.clear_node_tree(material.node_tree)
        nodes, links = node_tree.nodes, node_tree.links

        node_output = self.output_node(nodes, 0, 0)
        node_principled = self.principled_node(nodes, -400, 0)
        node_normal_map = self.normal_map_node(nodes, -600, -520)

        links.new(self.socket(node_output, "Surface"), self.socket(node_principled, "BSDF"))
        links.new(self.socket(node_principled, "Normal"), self.socket(node_normal_map, "Normal"))

        textures = [
            ["n", -900, -520, "Color", node_normal_map, "Color", 'NORMAL'],
            ["d", -900, -100, "Color", node_principled, "Base Color", 'EMIT'],
            ["r", -900, -260, "Color", node_principled, "Roughness", 'EMIT'],
            ["m", -900, -180, "Color", node_principled, "Metallic", 'EMIT'],
            ["e", -900, -440, "Color", node_principled, "Emission", 'EMIT'],
        ]

        wm = bpy.context.window_manager
        wm.progress_begin(0, 100)
        wm.progress_update(0)

        for t in textures:
            image = self.verify_image(settings, path, active.name + "_" + t[0])
            node_image = self.image_node(nodes, image, t[1], t[2])
            links.new(self.socket(node_image, t[3]), self.socket(t[4], t[5]))

            nodes_to_delete = []

            for n in selected_nodes:
                if t[0] in "drm":
                    socket_emission = self.socket(n[1], "Emission")
                    socket_drm_in = self.socket(n[1], t[5])

                    if socket_drm_in.links:
                        socket_drm_out = socket_drm_in.links[0].from_socket
                        n[0].links.new(socket_emission, socket_drm_out)

                    elif t[0] in "d":
                        socket_rgb = n[0].nodes.new("ShaderNodeRGB").outputs[0]
                        socket_rgb.default_value = socket_drm_in.default_value
                        n[0].links.new(socket_emission, socket_rgb)
                        nodes_to_delete.append([n[0].nodes, socket_rgb.node])

                    elif t[0] in "rm":
                        socket_value = n[0].nodes.new("ShaderNodeValue").outputs[0]
                        socket_value.default_value = socket_drm_in.default_value
                        n[0].links.new(socket_emission, socket_value)
                        nodes_to_delete.append([n[0].nodes, socket_value.node])

                elif t[0] in "e":
                    for n in selected_nodes:
                        socket_emission = self.socket(n[1], "Emission")
                        original_emission = n[3]

                        if original_emission:
                            n[0].links.new(socket_emission, original_emission)

                        elif socket_emission.links:
                            n[0].links.remove(socket_emission.links[0])

            nodes.active = node_image
            self.bake(settings, t[6])
            self.save_image(context, image)

            for n in nodes_to_delete:
                n[0].remove(n[1])

            wm.progress_update((textures.index(t)+1)*20)

        wm.progress_end()
        return {'FINISHED'}


class BakePanel(bpy.types.Panel):
    """Panel for baking"""
    bl_idname = "BEDSET_PT_BakePanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Bedset"
    bl_label = "Baking"

    def draw(self, context):
        settings = context.scene.BedsetBakeSettings
        self.layout.operator(Bake.bl_idname)
        self.layout.prop(settings, "cage")
        self.layout.prop(settings, "width")
        self.layout.prop(settings, "height")
        self.layout.prop(settings, "margin")
