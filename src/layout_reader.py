from src.layout import *


class DashLayoutReader:
    STR_TO_OBJECT_TYPE = {
        "b" : DashObjectType.BLOCK,
        "us" : DashObjectType.UP_SPIKE,
        "rs" : DashObjectType.RIGHT_SPIKE,
        "ds" : DashObjectType.DOWN_SPIKE,
        "ls" : DashObjectType.LEFT_SPIKE,
        "yo" : DashObjectType.YELLOW_ORB,
        "po" : DashObjectType.PINK_ORB,
        "bo" : DashObjectType.BLUE_ORB,
        "go" : DashObjectType.GREEN_ORB,
        "ro" : DashObjectType.RED_ORB,
        "ko" : DashObjectType.BLACK_ORB
    }


    @staticmethod
    def create_default_layout() -> DashLayout:
        return DashLayout(objects=[
            DashObject(DashObjectType.DOWN_SPIKE, (17 , 0)),
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

    @classmethod
    def read_layout_from_csv(cls, file_path: str) -> DashLayout:
        objects = []
        with open(file_path, 'r') as file:
            skip_first = True
            for line in file:
                if skip_first:
                    skip_first = False
                    continue

                parts = line.strip().split(',')
                if len(parts) != 3:
                    continue

                obj_type = cls.STR_TO_OBJECT_TYPE[parts[0].strip()]
                position = (float(parts[1].strip()), float(parts[2].strip()))
                objects.append(DashObject(obj_type, position))

                print(obj_type, position)

        return DashLayout(objects=objects)