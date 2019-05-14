import bpy
import os
import pathlib


class ExportObj(bpy.types.Operator):
    """Export selected objects to Obj files"""
    bl_idname = "bedset.export_obj"
    bl_label = "Export Obj"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return bpy.data.is_saved and len(context.selected_objects) > 0

    def execute(self, context):
        blend = pathlib.Path(bpy.data.filepath)
        folder = str(blend.resolve().parent)

        selected = []
        for o in context.selected_objects:
            selected.append(o)
            o.select_set(False)

        for o in selected:
            if o.type != 'MESH':
                continue

            o.select_set(True)

            obj = folder + os.sep + o.name + ".obj"
            bpy.ops.export_scene.obj(
                filepath=obj,
                check_existing=False,
                axis_forward='-Z',
                axis_up='Y',
                filter_glob="*.obj",
                use_selection=True,
                use_animation=False,
                use_mesh_modifiers=True,
                use_edges=True,
                use_smooth_groups=True,
                use_smooth_groups_bitflags=True,
                use_normals=True,
                use_uvs=True,
                use_materials=False,
                use_triangles=False,
                use_nurbs=False,
                use_vertex_groups=False,
                use_blen_objects=True,
                group_by_object=False,
                group_by_material=False,
                keep_vertex_order=False,
                global_scale=1,
                path_mode='AUTO',
            )

            o.select_set(False)

        for o in selected:
            o.select_set(True)

        return {'FINISHED'}
