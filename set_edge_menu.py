import bpy
from . set_edge import SetEdge


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
