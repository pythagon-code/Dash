from layout import *
from velocity import DashVelocity


HITBOX_ORB = 0.75

class DashPhysics:

    GRAVITY = 1
    MAX_SPEED = 2
    GAME_SPEED = 2


    HITBOX_SIZE = {
        DashObjectType.BLOCK: 1,
        DashObjectType.SPIKE: 0.9,
        DashObjectType.UPSIDE_DOWN_SPIKE: 0.9,
        DashObjectType.YELLOW_ORB: HITBOX_ORB,
        DashObjectType.PINK_ORB: HITBOX_ORB,
        DashObjectType.BLUE_ORB: HITBOX_ORB,
        DashObjectType.GREEN_ORB: HITBOX_ORB,
        DashObjectType.RED_ORB: HITBOX_ORB,
        DashObjectType.BLACK_ORB: HITBOX_ORB
    }

    REBOUND_FRAMES = 20


    def __init__(self, layout: DashLayout) -> None:
        self.layout = layout
        self.cube_position = (7.5, 0)
        self.cube_velocity = DashVelocity()
        self.line = -10
        self.died = False
        self.rebound = 0
        self.falling = False


    def is_cube_touching(self, obj: DashObject) -> bool:
        touch_distance = self.HITBOX_SIZE[obj.objectType]
        real_dist_x = abs(self.cube_position[0] + self.line - obj.position[0])
        real_dist_y = abs(self.cube_position[1] - obj.position[1])
        # print(f"real_dist_x: {real_dist_x}, real_dist_y: {real_dist_y}, touch_distance: {touch_distance}, cube_pos: {self.cube_position}, obj_pos: {obj.position}")
        return real_dist_x < touch_distance and real_dist_y < touch_distance


    def is_cube_grounded(self, obj: DashObject) -> bool:
        assert obj.objectType == DashObjectType.BLOCK
        grounded_distance = 1.01
        threshold = 0.25
        lower_bound = grounded_distance - threshold
        above = (self.cube_position[1] > obj.position[1]) ^ self.cube_velocity.reversed_gravity
        real_dist_x = abs(self.cube_position[0] + self.line - obj.position[0])
        real_dist_y = abs(self.cube_position[1] - obj.position[1])
        # print(above, real_dist_x, real_dist_y, grounded_distance, lower_bound)
        return above and real_dist_x < grounded_distance and lower_bound < real_dist_y <= grounded_distance


    def step(self, jump: bool, just_jump: bool, restart: bool) -> None:
        if self.cube_position[1] > 20 or self.cube_position[1] <= 0 and self.cube_velocity.reversed_gravity:
            self.died = True
            return

        while self.layout.should_remove_leftmost_object(self.line):
            self.layout.remove_leftmost_object()

        self.falling = self.cube_position[1] != 0 or self.cube_velocity.reversed_gravity

        self.cube_position = self.cube_position[0], max(0, self.cube_position[1] + self.cube_velocity.velocity)

        for obj in self.layout.objects:
            if not DashLayout.should_display_object(obj, self.line):
                break

            if obj.objectType == DashObjectType.SPIKE or obj.objectType == DashObjectType.UPSIDE_DOWN_SPIKE:
                if self.is_cube_touching(obj):
                    self.died = True
            elif obj.objectType == DashObjectType.BLOCK:
                if self.is_cube_grounded(obj):
                    self.falling = False
                    self.cube_velocity.set_speed(0)
                    unit = -1 if self.cube_velocity.reversed_gravity else 1
                    self.cube_position = self.cube_position[0], obj.position[1] + unit
                    self.rebound = 0
                elif self.is_cube_touching(obj):
                    self.died = True

            elif self.rebound == 0 and just_jump and self.is_cube_touching(obj):
                if obj.objectType == DashObjectType.YELLOW_ORB:
                    self.cube_velocity.set_speed(0.25)
                    self.rebound = self.REBOUND_FRAMES
                elif obj.objectType == DashObjectType.PINK_ORB:
                    self.cube_velocity.set_speed(0.2)
                    self.rebound = self.REBOUND_FRAMES
                elif obj.objectType == DashObjectType.BLUE_ORB:
                    self.cube_velocity.reverse_gravity()
                    self.rebound = self.REBOUND_FRAMES
                elif obj.objectType == DashObjectType.GREEN_ORB:
                    self.cube_velocity.reverse_gravity()
                    self.cube_velocity.set_speed(0.25)
                    self.rebound = self.REBOUND_FRAMES
                elif obj.objectType == DashObjectType.RED_ORB:
                    self.cube_velocity.set_speed(0.32)
                    self.rebound = self.REBOUND_FRAMES
                elif obj.objectType == DashObjectType.BLACK_ORB:
                    self.cube_velocity.set_speed(-0.4)
                    self.rebound = self.REBOUND_FRAMES

        if self.falling:
            self.cube_velocity.fall()

        # print(f"velocity: {self.cube_velocity.velocity}")
        if jump and not self.falling and self.rebound == 0:
            self.cube_velocity.set_speed(0.25)
            self.rebound = self.REBOUND_FRAMES
        elif self.rebound > 0:
            self.rebound -= 1

        self.line += 0.08173