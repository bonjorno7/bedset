import bpy

from . booleans . edit import EditBoolean
from . booleans . mod import ModBoolean

from . modifiers . bevel import Bevel
from . modifiers . solidify import Solidify
from . modifiers . apply import ApplyModifiers

from . object . auto_smooth import AutoSmooth
from . object . export_obj import ExportObj

from . edges . get_angle import GetAngle
from . edges . get_edge import GetEdge
from . edges . set_edge import SetEdge


def in_edit_mode(context):
    active = context.active_object
    return active is not None and active.mode == 'EDIT'


class BooleansMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_BooleansMenu"
    bl_label = "Booleans"

    def draw(self, context):
        pie = self.layout.menu_pie()

        if in_edit_mode(context):
            pie.operator(EditBoolean.bl_idname, text="(D) Difference", icon='SELECT_SUBTRACT').kind = 'DIFFERENCE'
            pie.operator(EditBoolean.bl_idname, text="(U) Union", icon='SELECT_EXTEND').kind = 'UNION'
            pie.operator(EditBoolean.bl_idname, text="(C) Cut", icon='MOD_OPACITY').kind = 'CUT'
            pie.operator(EditBoolean.bl_idname, text="(I) Intersect", icon='SELECT_INTERSECT').kind = 'INTERSECT'

        else:
            pie.operator(ModBoolean.bl_idname, text="(D) Difference", icon='SELECT_SUBTRACT').kind = 'DIFFERENCE'
            pie.operator(ModBoolean.bl_idname, text="(U) Union", icon='SELECT_EXTEND').kind = 'UNION'
            pie.operator(ModBoolean.bl_idname, text="(N) Inset", icon='MOD_SOLIDIFY').kind = 'INSET'
            pie.operator(ModBoolean.bl_idname, text="(I) Intersect", icon='SELECT_INTERSECT').kind = 'INTERSECT'
            pie.operator(ModBoolean.bl_idname, text="(E) Extract", icon='MOD_OPACITY').kind = 'EXTRACT'


class CallBooleansMenu(bpy.types.Operator):
    """Open the Booleans pie menu"""
    bl_idname = "bedset.call_booleans_menu"
    bl_label = "Booleans"

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name=BooleansMenu.bl_idname)
        return {'FINISHED'}


class ModifiersMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_ModifiersMenu"
    bl_label = "Modifiers"

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.operator(Bevel.bl_idname, text="(B) Bevel", icon='MOD_BEVEL')
        pie.operator(Solidify.bl_idname, text="(Y) Solidify", icon='MOD_SOLIDIFY')
        pie.operator(ApplyModifiers.bl_idname, text="(A) Apply", icon='CHECKBOX_HLT')
        # TODO: Mirror, Array, Circular Array


class CallModifiersMenu(bpy.types.Operator):
    """Open the Modifiers pie menu"""
    bl_idname = "bedset.call_modifiers_menu"
    bl_label = "Call Modifiers Menu"

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name=ModifiersMenu.bl_idname)
        return {'FINISHED'}


class SetOriginMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_SetOriginMenu"
    bl_label = "Set Origin"

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.operator("object.origin_set", text="(G) Geometry to Origin").type = 'GEOMETRY_ORIGIN'
        pie.operator("object.origin_set", text="(O) Origin to Geometry").type = 'ORIGIN_GEOMETRY'
        pie.operator("object.origin_set", text="(C) Origin to 3D Cursor").type = 'ORIGIN_CURSOR'
        pie.operator("object.origin_set", text="(M) Origin to Center of Mass").type = 'ORIGIN_CENTER_OF_MASS'
        pie.operator("object.origin_set", text="(V) Origin to Center of Volume").type = 'ORIGIN_CENTER_OF_VOLUME'


class CallSetOriginMenu(bpy.types.Operator):
    """Open the Set Origin menu"""
    bl_idname = "bedset.call_set_origin_menu"
    bl_label = "Call Set Origin Menu"

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name=SetOriginMenu.bl_idname)
        return {'FINISHED'}


class ApplyTransformsMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_ApplyTransformsMenu"
    bl_label = "Apply Transforms"

    def draw(self, context):
        pie = self.layout.menu_pie()
        op = pie.operator("object.transform_apply", text="(L) Location")
        op.location, op.rotation, op.scale, op.properties = True, False, False, False
        op = pie.operator("object.transform_apply", text="(S) Scale")
        op.location, op.rotation, op.scale, op.properties = False, False, True, False
        op = pie.operator("object.transform_apply", text="(P) Properties")
        op.location, op.rotation, op.scale, op.properties = False, False, False, True
        op = pie.operator("object.transform_apply", text="(R) Rotation")
        op.location, op.rotation, op.scale, op.properties = False, True, False, False
        op = pie.operator("object.transform_apply", text="(A) All Transforms")
        op.location, op.rotation, op.scale, op.properties = True, True, True, False
        op = pie.operator("object.transform_apply", text="(O) Rotation and Scale")
        op.location, op.rotation, op.scale, op.properties = False, True, True, False


class CallApplyTransformsMenu(bpy.types.Operator):
    """Open the Apply Transforms menu"""
    bl_idname = "bedset.call_apply_transforms_menu"
    bl_label = "Call Apply Transforms Menu"

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name=ApplyTransformsMenu.bl_idname)
        return {'FINISHED'}


class ObjectMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_ObjectMenu"
    bl_label = "Object"

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.operator(AutoSmooth.bl_idname, text="(S) Auto Smooth", icon='MATSHADERBALL')
        pie.operator(ExportObj.bl_idname, text="(E) Export OBJ", icon='EXPORT')
        pie.operator(CallSetOriginMenu.bl_idname, text="(O) Set Origin", icon='OBJECT_ORIGIN')
        pie.operator(CallApplyTransformsMenu.bl_idname, text="(A) Apply Transforms", icon='CHECKBOX_HLT')
        # TODO: Make pie menus for Set Origin and Apply Transforms


class CallObjectMenu(bpy.types.Operator):
    """Open the Object pie menu"""
    bl_idname = "bedset.call_object_menu"
    bl_label = "Call Object Menu"

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name=ObjectMenu.bl_idname)
        return {'FINISHED'}


class SelectEdgesMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_SelectEdgesMenu"
    bl_label = "Select Edges"

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.operator(GetEdge.bl_idname, text="(S) Seam").kind = 'SEAM'
        pie.operator(GetEdge.bl_idname, text="(H) Sharp").kind = 'SHARP'
        pie.operator(GetEdge.bl_idname, text="(B) Bevel").kind = 'BEVEL'
        pie.operator(GetEdge.bl_idname, text="(C) Crease").kind = 'CREASE'
        pie.operator(GetAngle.bl_idname, text="(A) Angle")


class CallSelectEdgesMenu(bpy.types.Operator):
    """Open the Select Edges pie menu"""
    bl_idname = "bedset.call_select_edges_menu"
    bl_label = "Call Select Edges Menu"

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name=SelectEdgesMenu.bl_idname)
        return {'FINISHED'}


class SelectEdgesInvertedMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_SelectEdgesInvertedMenu"
    bl_label = "Select Edges Inverted"

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.operator(GetEdge.bl_idname, text="(S) Seam").kind = 'NOT_SEAM'
        pie.operator(GetEdge.bl_idname, text="(H) Sharp").kind = 'NOT_SHARP'
        pie.operator(GetEdge.bl_idname, text="(B) Bevel").kind = 'NOT_BEVEL'
        pie.operator(GetEdge.bl_idname, text="(C) Crease").kind = 'NOT_CREASE'
        pie.operator(GetEdge.bl_idname, text="(X) Any").kind = 'NOT_ANY'


class CallSelectEdgesInvertedMenu(bpy.types.Operator):
    """Open the Select Edges Inverted pie menu"""
    bl_idname = "bedset.call_select_edges_inverted_menu"
    bl_label = "Call Select Edges Inverted Menu"

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name=SelectEdgesInvertedMenu.bl_idname)
        return {'FINISHED'}


class MarkEdgesMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_MarkEdgesMenu"
    bl_label = "Mark Edges"

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.operator(SetEdge.bl_idname, text="(S) Seam").kind = 'MARK_SEAM'
        pie.operator(SetEdge.bl_idname, text="(H) Sharp").kind = 'MARK_SHARP'
        pie.operator(SetEdge.bl_idname, text="(B) Bevel").kind = 'MARK_BEVEL'
        pie.operator(SetEdge.bl_idname, text="(C) Crease").kind = 'MARK_CREASE'


class CallMarkEdgesMenu(bpy.types.Operator):
    """Open the Mark Edges pie menu"""
    bl_idname = "bedset.call_mark_edges_menu"
    bl_label = "Call Mark Edges Menu"

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name=MarkEdgesMenu.bl_idname)
        return {'FINISHED'}


class ClearEdgesMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_ClearEdgesMenu"
    bl_label = "Clear Edges"

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.operator(SetEdge.bl_idname, text="(S) Seam").kind = 'CLEAR_SEAM'
        pie.operator(SetEdge.bl_idname, text="(H) Sharp").kind = 'CLEAR_SHARP'
        pie.operator(SetEdge.bl_idname, text="(B) Bevel").kind = 'CLEAR_BEVEL'
        pie.operator(SetEdge.bl_idname, text="(C) Crease").kind = 'CLEAR_CREASE'
        pie.operator(SetEdge.bl_idname, text="(X) All").kind = 'CLEAR_ALL'


class CallClearEdgesMenu(bpy.types.Operator):
    """Open the Clear Edges pie menu"""
    bl_idname = "bedset.call_clear_edges_menu"
    bl_label = "Call Clear Edges Menu"

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name=ClearEdgesMenu.bl_idname)
        return {'FINISHED'}


class EdgesMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_EdgesMenu"
    bl_label = "Edges"

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.operator(CallSelectEdgesMenu.bl_idname, text="(S) Select", icon='ZOOM_IN')
        pie.operator(CallSelectEdgesInvertedMenu.bl_idname, text="(I) Select Inverted", icon='ZOOM_OUT')
        pie.operator(CallMarkEdgesMenu.bl_idname, text="(M) Mark", icon='ADD')
        pie.operator(CallClearEdgesMenu.bl_idname, text="(C) Clear", icon='REMOVE')


class CallEdgesMenu(bpy.types.Operator):
    """Open the Edges pie menu"""
    bl_idname = "bedset.call_edges_menu"
    bl_label = "Call Edges Menu"

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name=EdgesMenu.bl_idname)
        return {'FINISHED'}


class BedsetMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_BedsetMenu"
    bl_label = "Bedset"

    def draw(self, context):
        pie = self.layout.menu_pie()

        pie.operator(CallBooleansMenu.bl_idname, text="(B) Booleans", icon='MOD_BOOLEAN')
        pie.operator(CallModifiersMenu.bl_idname, text="(M) Modifiers", icon='MODIFIER')
        pie.operator(CallObjectMenu.bl_idname, text="(O) Object", icon='OBJECT_DATA')

        if in_edit_mode(context):
            pie.operator(CallEdgesMenu.bl_idname, text="(E) Edges", icon='EDGESEL')
