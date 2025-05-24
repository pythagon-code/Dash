from layout import *


class DashLayoutCreator:
    @staticmethod
    def create_default_layout() -> DashLayout:
        return DashLayout(objects=[
            DashObject(DashObjectType.UPSIDE_DOWN_SPIKE, (12, 0)),
            DashObject(DashObjectType.BLOCK, (13, 1)),
            DashObject(DashObjectType.BLOCK, (14, 1)),
            DashObject(DashObjectType.BLOCK, (15, 1)),
            DashObject(DashObjectType.BLOCK, (16, 1)),
            DashObject(DashObjectType.BLOCK, (17, 1)),
            DashObject(DashObjectType.BLUE_ORB, (19, 4)),
            DashObject(DashObjectType.BLOCK, (20, 6)),
            DashObject(DashObjectType.BLOCK, (21, 6)),
            DashObject(DashObjectType.RED_ORB, (25, 6))
        ])