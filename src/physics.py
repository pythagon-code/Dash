from layout import *
from velocity import DashVelocity


class DashPhysics:

    GRAVITY = 1
    MAX_SPEED = 2
    GAME_SPEED = 2


    HITBOX_SIZE = {
        DashObjectType.BLOCK: 1,
        DashObjectType.SPIKE: 0.9,
        DashObjectType.UPSIDE_DOWN_SPIKE: 0.9,
        DashObjectType.YELLOW_ORB: 0.9,
        DashObjectType.PINK_ORB: 0.9,
        DashObjectType.BLUE_ORB: 0.9,
        DashObjectType.RED_ORB: 0.9
    }

    REBOUND_FRAMES = 100


    def __init__(self, layout: DashLayout) -> None:
        self.layout = layout
        self.cube_position = (7.5, 0)
        self.cube_velocity = DashVelocity()
        self.grounded = True
        self.line = -10
        self.died = False
        self.rebound = 0


    def is_cube_touching(self, obj: DashObject) -> bool:
        touch_distance = self.HITBOX_SIZE[obj.objectType]
        real_dist_x = abs(self.cube_position[0] + self.line - obj.position[0])
        real_dist_y = abs(self.cube_position[1] - obj.position[1])
        # print(f"real_dist_x: {real_dist_x}, real_dist_y: {real_dist_y}, touch_distance: {touch_distance}, cube_pos: {self.cube_position}, obj_pos: {obj.position}")
        return real_dist_x < touch_distance and real_dist_y < touch_distance


    def is_cube_grounded(self, obj: DashObject) -> bool:
        assert obj.objectType == DashObjectType.BLOCK
        grounded_distance = 0
        above = self.cube_position[1] > obj.position[1]
        real_dist_y = abs(self.cube_position[1] - obj.position[1])
        return above ^ self.cube_velocity.reversed_gravity and real_dist_y < grounded_distance


    def step(self, jump: bool, just_jump: bool, restart: bool) -> None:
        while self.layout.should_remove_leftmost_object(self.line):
            self.layout.remove_leftmost_object()

        falling = self.cube_position[1] != 0

        for obj in self.layout.objects:
            if not DashLayout.should_display_object(obj, self.line):
                break

            if obj.objectType == DashObjectType.SPIKE or obj.objectType == DashObjectType.UPSIDE_DOWN_SPIKE:
                if self.is_cube_touching(obj):
                    self.died = True
            elif obj.objectType == DashObjectType.BLOCK:
                if self.is_cube_grounded(obj):
                    falling = False
                elif self.is_cube_grounded(obj):
                    self.died = True

        if falling:
            self.cube_velocity.fall()

        print(f"velocity: {self.cube_velocity.velocity}")
        self.cube_position = self.cube_position[0], max(0, self.cube_position[1] + self.cube_velocity.velocity)
        if jump and not falling and self.rebound == 0:
            self.cube_velocity.set_speed(0.25)
            self.rebound = self.REBOUND_FRAMES
        elif self.rebound > 0:
            self.rebound -= 1


        self.line += 0.07173