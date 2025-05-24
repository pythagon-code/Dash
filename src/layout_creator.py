from layout import *


class DashLayoutCreator:
    @staticmethod
    def create_default_layout() -> DashLayout:
        return DashLayout(objects=[
            DashObject(DashObjectType.UPSIDE_DOWN_SPIKE, (12, 0)),
            DashObject(DashObjectType.BLOCK, (13, 1)),
        ])