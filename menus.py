import bpy
import math

from . edit_boolean import EditBoolean
from . mod_boolean import ModBoolean
from . auto_smooth import AutoSmooth

from . get_angle import GetAngle
from . get_edge import GetEdge
from . set_edge import SetEdge


class ApplyPie(bpy.types.Menu):
    bl_idname = "BEDSET_MT_ApplyPie"
    bl_label = "Bedset Apply Pie"

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.separator()
        pie.separator()
        op = pie.operator("object.transform_apply", text="All Transforms")
        op.location, op.rotation, op.scale, op.properties = True, True, True, False
        op = pie.operator("object.transform_apply", text="Rotation")
        op.location, op.rotation, op.scale, op.properties = False, True, False, False
        op = pie.operator("object.transform_apply", text="Location")
        op.location, op.rotation, op.scale, op.properties = True, False, False, False
        op = pie.operator("object.transform_apply", text="Scale")
        op.location, op.rotation, op.scale, op.properties = False, False, True, False
        op = pie.operator("object.transform_apply", text="Rotation and Scale")
        op.location, op.rotation, op.scale, op.properties = False, True, True, False
        pie.operator("object.convert", text="Visual Geometry to Mesh").target = 'MESH'


class OriginPie(bpy.types.Menu):
    bl_idname = "BEDSET_MT_OriginPie"
    bl_label = "Bedset Origin Pie"

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.separator()
        pie.separator()
        pie.separator()
        pie.operator("object.origin_set", text="Origin to 3D Cursor").type = 'ORIGIN_CURSOR'
        pie.separator()
        pie.separator()
        pie.operator("object.origin_set", text="Geometry to Origin").type = 'GEOMETRY_ORIGIN'
        pie.operator("object.origin_set", text="Origin to Geometry").type = 'ORIGIN_GEOMETRY'


class ShadingPie(bpy.types.Menu):
    bl_idname = "BEDSET_MT_ShadingPie"
    bl_label = "Bedset Shading Pie"

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.separator()
        pie.separator()
        pie.operator("mesh.customdata_custom_splitnormals_clear", text="Clear Custom Normals")
        pie.operator(AutoSmooth.bl_idname, text="Auto Smooth 60").angle = math.radians(60)
        pie.operator(AutoSmooth.bl_idname, text="Auto Smooth 30").angle = math.radians(30)
        pie.operator(AutoSmooth.bl_idname, text="Auto Smooth 180").angle = math.radians(180)
        pie.operator("object.shade_flat", text="Shade Flat")
        pie.operator("object.shade_smooth", text="Shade Smooth")


class ViewPie(bpy.types.Menu):
    bl_idname = "BEDSET_MT_ViewPie"
    bl_label = "Bedset View Pie"

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.prop(bpy.context.space_data.overlay, "show_overlays", text="Overlays")
        pie.prop(bpy.context.space_data.overlay, "show_wireframes", text="Wireframes")
        pie.operator("view3d.view_persportho", text="Perspecive / Ortho")
        pie.operator("view3d.view_camera", text="View Camera")


class ModBooleanPie(bpy.types.Menu):
    bl_idname = "BEDSET_MT_ModBooleanPie"
    bl_label = "Bedset Mod Boolean Pie"

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.separator()
        pie.separator()
        pie.separator()
        pie.operator(ModBoolean.bl_idname, text="Union").kind = 'UNION'
        pie.operator(ModBoolean.bl_idname, text="Difference").kind = 'DIFFERENCE'
        pie.operator(ModBoolean.bl_idname, text="Intersect").kind = 'INTERSECT'
        pie.operator(ModBoolean.bl_idname, text="Slice").kind = 'SLICE'
        pie.operator(ModBoolean.bl_idname, text="Inset").kind = 'INSET'


class EditBooleanPie(bpy.types.Menu):
    bl_idname = "BEDSET_MT_EditBooleanPie"
    bl_label = "Bedset Edit Boolean Pie"

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.separator()
        pie.separator()
        pie.separator()
        pie.operator(EditBoolean.bl_idname, text="Union").kind = 'UNION'
        pie.operator(EditBoolean.bl_idname, text="Difference").kind = 'DIFFERENCE'
        pie.operator(EditBoolean.bl_idname, text="Intersect").kind = 'INTERSECT'
        pie.operator(EditBoolean.bl_idname, text="Slice").kind = 'SLICE'
        pie.operator(EditBoolean.bl_idname, text="Cut").kind = 'CUT'


class DeletePie(bpy.types.Menu):
    bl_idname = "BEDSET_MT_DeletePie"
    bl_label = "Bedset Delete Pie"

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.separator()
        pie.separator()
        pie.operator("mesh.dissolve_edges", text="Dissolve Edges")
        pie.operator("mesh.delete", text="Delete Edges").type = 'EDGE'
        pie.operator("mesh.delete", text="Delete Vertices").type = 'VERT'
        pie.operator("mesh.delete", text="Delete Faces").type = 'FACE'
        pie.operator("mesh.dissolve_verts", text="Dissolve Vertices")
        pie.operator("mesh.dissolve_faces", text="Dissolve Faces")


class VertexPie(bpy.types.Menu):
    bl_idname = "BEDSET_MT_VertexPie"
    bl_label = "Bedset Vertex Pie"

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.separator()
        pie.separator()
        pie.separator()
        pie.operator("mesh.remove_doubles", text="Merge By Distance")
        pie.operator("mesh.merge", text="Merge At Center").type = 'CENTER'
        try:
            pie.operator("mesh.merge", text="Merge At Last").type = 'LAST'
        except:
            pass
        pie.operator("mesh.vert_connect_path", text="Connect Path")
        pie.operator("mesh.knife_tool", text="Knife Tool")


class EdgeSelectMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_EdgeSelectMenu"
    bl_label = "Bedset Edge Select Menu"

    def draw(self, context):
        self.layout.operator(GetAngle.bl_idname, text="Select By Angle")
        self.layout.operator(GetEdge.bl_idname, text="Select By Seam").kind = 'SEAM'
        self.layout.operator(GetEdge.bl_idname, text="Select By Sharp").kind = 'SHARP'
        self.layout.operator(GetEdge.bl_idname, text="Select By Bevel").kind = 'BEVEL'
        self.layout.operator(GetEdge.bl_idname, text="Select By Crease").kind = 'CREASE'
        self.layout.separator()
        self.layout.operator(GetEdge.bl_idname, text="Select Not Any").kind = 'NOT_ANY'
        self.layout.operator(GetEdge.bl_idname, text="Select Not Seam").kind = 'NOT_SEAM'
        self.layout.operator(GetEdge.bl_idname, text="Select Not Sharp").kind = 'NOT_SHARP'
        self.layout.operator(GetEdge.bl_idname, text="Select Not Bevel").kind = 'NOT_BEVEL'
        self.layout.operator(GetEdge.bl_idname, text="Select Not Crease").kind = 'NOT_CREASE'


class EdgeMarkMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_EdgeMarkMenu"
    bl_label = "Bedset Edge Mark Menu"

    def draw(self, context):
        self.layout.operator(SetEdge.bl_idname, text="Mark Seam And Sharp").kind = 'MARK_SEAM_AND_SHARP'
        self.layout.operator(SetEdge.bl_idname, text="Mark Seam").kind = 'MARK_SEAM'
        self.layout.operator(SetEdge.bl_idname, text="Mark Sharp").kind = 'MARK_SHARP'
        self.layout.operator(SetEdge.bl_idname, text="Mark Bevel").kind = 'MARK_BEVEL'
        self.layout.operator(SetEdge.bl_idname, text="Mark Crease").kind = 'MARK_CREASE'
        self.layout.separator()
        self.layout.operator(SetEdge.bl_idname, text="Clear All").kind = 'CLEAR_ALL'
        self.layout.operator(SetEdge.bl_idname, text="Clear Seam").kind = 'CLEAR_SEAM'
        self.layout.operator(SetEdge.bl_idname, text="Clear Sharp").kind = 'CLEAR_SHARP'
        self.layout.operator(SetEdge.bl_idname, text="Clear Bevel").kind = 'CLEAR_BEVEL'
        self.layout.operator(SetEdge.bl_idname, text="Clear Crease").kind = 'CLEAR_CREASE'


class EdgePie(bpy.types.Menu):
    bl_idname = "BEDSET_MT_EdgePie"
    bl_label = "Bedset Edge Pie"

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.separator()
        pie.separator()
        pie.separator()
        pie.operator("mesh.bevel", text="Bevel Edges")
        pie.operator("mesh.bridge_edge_loops", text="Bridge Edge Loops").use_merge = False
        pie.operator("mesh.bridge_edge_loops", text="Merge Edge Loops").use_merge = True
        pie.operator("wm.call_menu", text="Select Menu").name = EdgeSelectMenu.bl_idname
        pie.operator("wm.call_menu", text="Mark Menu").name = EdgeMarkMenu.bl_idname


class FaceSelectMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_FaceSelectMenu"
    bl_label = "Bedset Face Select Menu"

    def draw(self, context):
        op = self.layout.operator("mesh.select_face_by_sides", text="Select Triangles")
        op.type, op.number = 'EQUAL', 3
        op = self.layout.operator("mesh.select_face_by_sides", text="Select Quads")
        op.type, op.number = 'EQUAL', 4
        op = self.layout.operator("mesh.select_face_by_sides", text="Select Ngons")
        op.type, op.number = 'GREATER', 4


class FacePie(bpy.types.Menu):
    bl_idname = "BEDSET_MT_FacePie"
    bl_label = "Bedset Face Pie"

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.separator()
        pie.separator()
        pie.operator("wm.call_menu", text="Select Menu").name = FaceSelectMenu.bl_idname
        pie.operator("mesh.quads_convert_to_tris", text="Triangulate Faces")
        pie.operator("mesh.poke", text="Poke Faces")
        pie.operator("mesh.inset", text="Inset Faces")
        pie.operator("mesh.flip_normals", text="Flip Normals")
        pie.operator("mesh.normals_make_consistent", text="Recalculate Normals")


class BedsetPie(bpy.types.Menu):
    bl_idname = "BEDSET_MT_BedsetPie"
    bl_label = "Bedset Pie"

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.operator("wm.call_menu_pie", text="Apply Pie", icon='OBJECT_DATA').name = ApplyPie.bl_idname
        pie.operator("wm.call_menu_pie", text="Origin Pie", icon='OBJECT_ORIGIN').name = OriginPie.bl_idname
        pie.operator("wm.call_menu_pie", text="Shading Pie", icon='MATSHADERBALL').name = ShadingPie.bl_idname
        pie.operator("wm.call_menu_pie", text="View Pie", icon='RESTRICT_VIEW_OFF').name = ViewPie.bl_idname
