import bpy

from . edit_boolean import EditBoolean

from . get_angle import GetAngle
from . get_edge import GetEdge

from . set_edge import SetEdge

from . object_boolean import ObjectBoolean
from . apply_boolean import ApplyBoolean

from . auto_smooth import AutoSmooth
from . bevel_object import BevelObject
from . export_obj import ExportObj


class EditBooleanMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_EditBooleanMenu"
    bl_label = "Boolean"

    def draw(self, context):
        self.layout.operator(
            EditBoolean.bl_idname,
            text="Difference",
        ).kind = 'DIFFERENCE'

        self.layout.operator(
            EditBoolean.bl_idname,
            text="Union",
        ).kind = 'UNION'

        self.layout.operator(
            EditBoolean.bl_idname,
            text="Intersect",
        ).kind = 'INTERSECT'

        self.layout.operator(
            EditBoolean.bl_idname,
            text="Cut",
        ).kind = 'CUT'


class GetEdgeMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_GetEdgeMenu"
    bl_label = "Get Edge"

    def draw(self, context):
        self.layout.operator(
            GetAngle.bl_idname,
            text="By Angle",
        )

        self.layout.operator(
            GetEdge.bl_idname,
            text="By Seam",
        ).kind = 'SEAM'

        self.layout.operator(
            GetEdge.bl_idname,
            text="By Sharp",
        ).kind = 'SHARP'

        self.layout.operator(
            GetEdge.bl_idname,
            text="By Bevel",
        ).kind = 'BEVEL'

        self.layout.operator(
            GetEdge.bl_idname,
            text="By Crease",
        ).kind = 'CREASE'

        self.layout.operator(
            GetEdge.bl_idname,
            text="By Not Seam",
        ).kind = 'NOT_SEAM'

        self.layout.operator(
            GetEdge.bl_idname,
            text="By Not Sharp",
        ).kind = 'NOT_SHARP'

        self.layout.operator(
            GetEdge.bl_idname,
            text="By Not Bevel",
        ).kind = 'NOT_BEVEL'

        self.layout.operator(
            GetEdge.bl_idname,
            text="By Not Crease",
        ).kind = 'NOT_CREASE'

        self.layout.operator(
            GetEdge.bl_idname,
            text="By Not Any",
        ).kind = 'NOT_ANY'


class SetEdgeMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_SetEdgeMenu"
    bl_label = "Set Edge"

    def draw(self, context):
        self.layout.operator(
            SetEdge.bl_idname,
            text="Mark Seam",
        ).kind = 'MARK_SEAM'

        self.layout.operator(
            SetEdge.bl_idname,
            text="Mark Sharp",
        ).kind = 'MARK_SHARP'

        self.layout.operator(
            SetEdge.bl_idname,
            text="Mark Bevel",
        ).kind = 'MARK_BEVEL'

        self.layout.operator(
            SetEdge.bl_idname,
            text="Mark Crease",
        ).kind = 'MARK_CREASE'

        self.layout.operator(
            SetEdge.bl_idname,
            text="Clear Seam",
        ).kind = 'CLEAR_SEAM'

        self.layout.operator(
            SetEdge.bl_idname,
            text="Clear Sharp",
        ).kind = 'CLEAR_SHARP'

        self.layout.operator(
            SetEdge.bl_idname,
            text="Clear Bevel",
        ).kind = 'CLEAR_BEVEL'

        self.layout.operator(
            SetEdge.bl_idname,
            text="Clear Crease",
        ).kind = 'CLEAR_CREASE'

        self.layout.operator(
            SetEdge.bl_idname,
            text="Clear All",
        ).kind = 'CLEAR_ALL'


class ObjectBooleanMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_ObjectBooleanMenu"
    bl_label = "Boolean"

    def draw(self, context):
        self.layout.operator(
            ObjectBoolean.bl_idname,
            text="Difference",
        ).kind = 'DIFFERENCE'

        self.layout.operator(
            ObjectBoolean.bl_idname,
            text="Union",
        ).kind = 'UNION'

        self.layout.operator(
            ObjectBoolean.bl_idname,
            text="Intersect",
        ).kind = 'INTERSECT'

        self.layout.operator(
            ApplyBoolean.bl_idname,
            text="Apply",
        )


class ExtraMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_ExtraMenu"
    bl_label = "Extra"

    def draw(self, context):
        self.layout.operator(AutoSmooth.bl_idname)
        self.layout.operator(BevelObject.bl_idname)
        self.layout.operator(ExportObj.bl_idname)


class BedsetMenu(bpy.types.Menu):
    bl_idname = "BEDSET_MT_BedsetMenu"
    bl_label = "Bedset"

    def draw(self, context):
        active = context.active_object

        if active is not None and active.mode == 'EDIT':
            self.layout.menu(EditBooleanMenu.bl_idname, icon='MOD_BOOLEAN')

            self.layout.separator()

            self.layout.menu(GetEdgeMenu.bl_idname, icon='EDGESEL')
            self.layout.menu(SetEdgeMenu.bl_idname, icon='EDGESEL')

        else:
            self.layout.menu(ObjectBooleanMenu.bl_idname, icon='MOD_BOOLEAN')

        self.layout.separator()

        self.layout.menu(ExtraMenu.bl_idname, icon='MONKEY')
