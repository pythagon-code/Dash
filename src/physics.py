from layout import *
from velocity import DashVelocity


class DashPhysics:

    GRAVITY = 1
    MAX_SPEED = 2
    GAME_SPEED = 2


    HITBOX_SIZE = {
        DashObjectType.BLOCK: 1,
        DashObjectType.SPIKE: 0.8,
        DashObjectType.UPSIDE_DOWN_SPIKE: 0.8,
        DashObjectType.YELLOW_ORB: 0.9,
        DashObjectType.PINK_ORB: 0.9,
        DashObjectType.BLUE_ORB: 0.9,
        DashObjectType.RED_ORB: 0.9
    }

    CUBE_HITBOX_SIZE = 25


    def __init__(self, layout: DashLayout) -> None:
        self.layout = layout
        self.cube_position = (7.5, 0)
        self.cube_velocity = DashVelocity()
        self.grounded = True
        self.line = -100
        self.died = False


    def is_cube_touching(self, obj: DashObject) -> bool:
        touch_distance = DashPhysics.HITBOX_SIZE[obj.objectType]
        real_dist_x = abs(self.cube_position[0] + self.line - obj.position[0])
        real_dist_y = abs(self.cube_position[1] - obj.position[1])
        print(f"real_dist_x: {real_dist_x}, real_dist_y: {real_dist_y}, touch_distance: {touch_distance}, cube_pos: {self.cube_position}, obj_pos: {obj.position}")
        return real_dist_x < touch_distance and real_dist_y < touch_distance


    def is_cube_grounded(self, obj: DashObject) -> bool:
        assert obj.objectType == DashObjectType.BLOCK
        grounded_distance = (DashPhysics.HITBOX_SIZE[obj.objectType] + 2 + DashPhysics.CUBE_HITBOX_SIZE) / 2
        above = self.cube_position[1] > obj.position[1]
        real_dist_y = abs(self.cube_position[1] - obj.position[1])
        return above ^ self.cube_velocity.reversed_gravity and real_dist_y < grounded_distance


    def step(self, jump: bool, just_jump: bool, restart: bool) -> None:
        while self.layout.should_remove_leftmost_object(self.line):
            self.layout.remove_leftmost_object()

        for obj in self.layout.objects:
            if not DashLayout.should_display_object(obj, self.line):
                break

            if obj.objectType == DashObjectType.SPIKE or obj.objectType == DashObjectType.UPSIDE_DOWN_SPIKE:
                if self.is_cube_touching(obj):
                    self.died = True

        self.line += 0.2