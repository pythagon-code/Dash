from enum import Enum
from collections import deque
from dataclasses import dataclass


class DashObjectType(Enum):
    BLOCK = 1
    SPIKE = 2
    UPSIDE_DOWN_SPIKE = 3
    YELLOW_ORB = 4
    PINK_ORB = 5
    BLUE_ORB = 6
    RED_ORB = 7


@dataclass
class DashObject:
    objectType: DashObjectType
    position: tuple[int, int]


class DashLayout:
    DESPAWN_ZONE = -100
    HIDE_ZONE = 1000


    def __init__(self, objects: list[DashObject]) -> None:
        self.objects: deque[DashObject] = deque(maxlen=9999)
        objects.sort(key=lambda o: o.position[0])

        for obj in objects:
            self.objects.append(obj)


    def should_remove_leftmost_object(self, line: float) -> bool:
        return len(self.objects) > 0 and self.objects[0].position[0] + line < DashLayout.DESPAWN_ZONE


    def remove_leftmost_object(self) -> DashObject:
        return self.objects.popleft()


    @staticmethod
    def should_display_object(obj: DashObject, line: float) -> bool:
        return obj.position[0] + line < DashLayout.HIDE_ZONE
