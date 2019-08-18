import bpy

from . booleans . edit import EditBoolean
from . booleans . mod import ModBoolean

from . modifiers . bevel import Bevel
from . modifiers . solidify import Solidify
from . modifiers . apply import Apply

from . object . auto_smooth import AutoSmooth
from . object . export_obj import ExportObj
from . object . move_origin import MoveOrigin

from . edges . get_angle import GetAngle
from . edges . get_edge import GetEdge
from . edges . set_edge import SetEdge


def in_edit_mode(context):
    active = context.active_object
    return active is not None and active.mode == 'EDIT'


class BooleansMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_BooleansMenu"
    bl_label = "(B) Booleans"
    bl_icon = 'MOD_BOOLEAN'

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
    bl_idname = "bedset.call_booleans_menu"
    bl_label = "(B) Booleans"
    bl_icon = 'MOD_BOOLEAN'

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name=BooleansMenu.bl_idname)
        return {'FINISHED'}


class ModifiersMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_ModifiersMenu"
    bl_label = "(M) Modifiers"
    bl_icon = 'MODIFIER'

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.operator(Bevel.bl_idname, text="(B) Bevel", icon='MOD_BEVEL')
        pie.operator(Solidify.bl_idname, text="(Y) Solidify", icon='MOD_SOLIDIFY')
        pie.operator(Apply.bl_idname, text="(A) Apply", icon='CHECKBOX_HLT')
        # TODO: Mirror, Array, Circular Array


class CallModifiersMenu(bpy.types.Operator):
    bl_idname = "bedset.call_modifiers_menu"
    bl_label = "(M) Modifiers"
    bl_icon = 'MODIFIER'

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name=ModifiersMenu.bl_idname)
        return {'FINISHED'}


class ObjectMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_ObjectMenu"
    bl_label = "(O) Object"
    bl_icon = 'OBJECT_DATA'

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.operator(AutoSmooth.bl_idname, text="(S) Auto Smooth", icon='MATSHADERBALL')
        pie.operator(ExportObj.bl_idname, text="(E) Export OBJ", icon='EXPORT')
        pie.operator(MoveOrigin.bl_idname, text="(O) Move Origin", icon='OBJECT_ORIGIN')


class CallObjectMenu(bpy.types.Operator):
    bl_idname = "bedset.call_object_menu"
    bl_label = "(O) Object"
    bl_icon = 'OBJECT_DATA'

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name=ObjectMenu.bl_idname)
        return {'FINISHED'}


class SelectEdgesMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_SelectEdgesMenu"
    bl_label = "(S) Select"
    bl_icon = 'ZOOM_IN'

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.operator(GetEdge.bl_idname, text="(S) Seam").kind = 'SEAM'
        pie.operator(GetEdge.bl_idname, text="(H) Sharp").kind = 'SHARP'
        pie.operator(GetEdge.bl_idname, text="(B) Bevel").kind = 'BEVEL'
        pie.operator(GetEdge.bl_idname, text="(C) Crease").kind = 'CREASE'
        pie.operator(GetAngle.bl_idname, text="(A) Angle")


class CallSelectEdgesMenu(bpy.types.Operator):
    bl_idname = "bedset.call_select_edges_menu"
    bl_label = "(S) Select"
    bl_icon = 'ZOOM_IN'

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name=SelectEdgesMenu.bl_idname)
        return {'FINISHED'}


class SelectEdgesInvertedMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_SelectEdgesInvertedMenu"
    bl_label = "(I) Select Inverted"
    bl_icon = 'ZOOM_OUT'

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.operator(GetEdge.bl_idname, text="(S) Seam").kind = 'NOT_SEAM'
        pie.operator(GetEdge.bl_idname, text="(H) Sharp").kind = 'NOT_SHARP'
        pie.operator(GetEdge.bl_idname, text="(B) Bevel").kind = 'NOT_BEVEL'
        pie.operator(GetEdge.bl_idname, text="(C) Crease").kind = 'NOT_CREASE'
        pie.operator(GetEdge.bl_idname, text="(X) Any").kind = 'NOT_ANY'


class CallSelectEdgesInvertedMenu(bpy.types.Operator):
    bl_idname = "bedset.call_select_edges_inverted_menu"
    bl_label = "(I) Select Inverted"
    bl_icon = 'ZOOM_OUTs'

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name=SelectEdgesInvertedMenu.bl_idname)
        return {'FINISHED'}


class MarkEdgesMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_MarkEdgesMenu"
    bl_label = "(M) Mark"
    bl_icon = 'ADD'

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.operator(SetEdge.bl_idname, text="(S) Seam").kind = 'MARK_SEAM'
        pie.operator(SetEdge.bl_idname, text="(H) Sharp").kind = 'MARK_SHARP'
        pie.operator(SetEdge.bl_idname, text="(B) Bevel").kind = 'MARK_BEVEL'
        pie.operator(SetEdge.bl_idname, text="(C) Crease").kind = 'MARK_CREASE'


class CallMarkEdgesMenu(bpy.types.Operator):
    bl_idname = "bedset.call_mark_edges_menu"
    bl_label = "(M) Mark"
    bl_icon = 'ADD'

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name=MarkEdgesMenu.bl_idname)
        return {'FINISHED'}


class ClearEdgesMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_ClearEdgesMenu"
    bl_label = "(C) Clear"
    bl_icon = 'REMOVE'

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.operator(SetEdge.bl_idname, text="(S) Seam").kind = 'CLEAR_SEAM'
        pie.operator(SetEdge.bl_idname, text="(H) Sharp").kind = 'CLEAR_SHARP'
        pie.operator(SetEdge.bl_idname, text="(B) Bevel").kind = 'CLEAR_BEVEL'
        pie.operator(SetEdge.bl_idname, text="(C) Crease").kind = 'CLEAR_CREASE'
        pie.operator(SetEdge.bl_idname, text="(X) All").kind = 'CLEAR_ALL'


class CallClearEdgesMenu(bpy.types.Operator):
    bl_idname = "bedset.call_clear_edges_menu"
    bl_label = "(C) Clear"
    bl_icon = 'REMOVE'

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name=ClearEdgesMenu.bl_idname)
        return {'FINISHED'}


class EdgesMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_EdgesMenu"
    bl_label = "(E) Edges"
    bl_icon = 'EDGESEL'

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.operator(CallSelectEdgesMenu.bl_idname, icon='ZOOM_IN')
        pie.operator(CallSelectEdgesInvertedMenu.bl_idname, icon='ZOOM_OUT')
        pie.operator(CallMarkEdgesMenu.bl_idname, icon='ADD')
        pie.operator(CallClearEdgesMenu.bl_idname, icon='REMOVE')


class CallEdgesMenu(bpy.types.Operator):
    bl_idname = "bedset.call_edges_menu"
    bl_label = "(E) Edges"
    bl_icon = 'EDGESEL'

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name=EdgesMenu.bl_idname)
        return {'FINISHED'}


class BedsetMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_BedsetMenu"
    bl_label = "(B) Bedset"
    bl_icon = 'BOLD'

    def draw(self, context):
        pie = self.layout.menu_pie()

        pie.operator(CallBooleansMenu.bl_idname, icon='MOD_BOOLEAN')
        pie.operator(CallModifiersMenu.bl_idname, icon='MODIFIER')
        pie.operator(CallObjectMenu.bl_idname, icon='OBJECT_DATA')

        if in_edit_mode(context):
            pie.operator(CallEdgesMenu.bl_idname, icon='EDGESEL')
