from src.layout import *
from src.velocity import DashVelocity

EDITOR_MODE = False

HITBOX_SPIKE = 0.7 if not EDITOR_MODE else 0
HITBOX_ORB = 0.75

class DashPhysics:

    GRAVITY = 1
    MAX_SPEED = 2
    GAME_SPEED = 2


    HITBOX_SIZE = {
        DashObjectType.BLOCK: 1 if not EDITOR_MODE else 0,
        DashObjectType.UP_SPIKE: HITBOX_SPIKE,
        DashObjectType.RIGHT_SPIKE: HITBOX_SPIKE,
        DashObjectType.DOWN_SPIKE: HITBOX_SPIKE,
        DashObjectType.LEFT_SPIKE: HITBOX_SPIKE,
        DashObjectType.YELLOW_ORB: HITBOX_ORB,
        DashObjectType.PINK_ORB: HITBOX_ORB,
        DashObjectType.BLUE_ORB: HITBOX_ORB,
        DashObjectType.GREEN_ORB: HITBOX_ORB,
        DashObjectType.RED_ORB: HITBOX_ORB,
        DashObjectType.BLACK_ORB: HITBOX_ORB
    }

    REBOUND_FRAMES = 20


    JUMP_FORCE = 0.22
    YELLOW_ORB_FORCE = 0.25
    PINK_ORB_FORCE = 0.2
    BLUE_ORB_FORCE = 0.25
    GREEN_ORB_FORCE = 0.25
    RED_ORB_FORCE = 0.32
    BLACK_ORB_FORCE = 0.4


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
        return real_dist_x < touch_distance and real_dist_y < touch_distance


    def is_cube_grounded(self, obj: DashObject) -> bool:
        assert obj.objectType == DashObjectType.BLOCK
        grounded_distance = 1.01
        threshold = 0.4
        lower_bound = grounded_distance - threshold
        above = (self.cube_position[1] > obj.position[1]) ^ self.cube_velocity.reversed_gravity
        real_dist_x = abs(self.cube_position[0] + self.line - obj.position[0])
        real_dist_y = abs(self.cube_position[1] - obj.position[1])
        return above and real_dist_x < grounded_distance and lower_bound < real_dist_y <= grounded_distance


    def step(self, jump: bool, just_jump: bool) -> None:
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

            if obj.objectType == DashObjectType.UP_SPIKE \
                or obj.objectType == DashObjectType.RIGHT_SPIKE \
                or obj.objectType == DashObjectType.DOWN_SPIKE \
                or obj.objectType == DashObjectType.LEFT_SPIKE \
            :
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
                    self.cube_velocity.set_speed(self.YELLOW_ORB_FORCE)
                    self.rebound = self.REBOUND_FRAMES
                elif obj.objectType == DashObjectType.PINK_ORB:
                    self.cube_velocity.set_speed(self.PINK_ORB_FORCE)
                    self.rebound = self.REBOUND_FRAMES
                elif obj.objectType == DashObjectType.BLUE_ORB:
                    self.cube_velocity.reverse_gravity()
                    self.rebound = self.REBOUND_FRAMES
                elif obj.objectType == DashObjectType.GREEN_ORB:
                    self.cube_velocity.reverse_gravity()
                    self.cube_velocity.set_speed(self.GREEN_ORB_FORCE)
                    self.rebound = self.REBOUND_FRAMES
                elif obj.objectType == DashObjectType.RED_ORB:
                    self.cube_velocity.set_speed(self.RED_ORB_FORCE)
                    self.rebound = self.REBOUND_FRAMES
                elif obj.objectType == DashObjectType.BLACK_ORB:
                    self.cube_velocity.set_speed(-self.BLACK_ORB_FORCE)
                    self.rebound = self.REBOUND_FRAMES

        if self.falling:
            self.cube_velocity.fall()

        if jump and not self.falling and self.rebound == 0:
            self.cube_velocity.set_speed(0.22)
            self.rebound = self.REBOUND_FRAMES
        elif self.rebound > 0:
            self.rebound -= 1

        self.line += 0.09173