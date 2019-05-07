import bpy
from . get_angle import GetAngle
from . get_edge import GetEdge


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
