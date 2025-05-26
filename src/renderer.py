import pygame.transform

from src.layout import *


class DashRenderer:
    ROTATE_SPEED = 4


    def __init__(self, game) -> None:
        from src.game import DashGame       # Prevent circular import
        self.game: DashGame = game
        self.rotated_cubes_images = [pygame.transform.rotate(self.game.cube, -i) for i in range(360)]
        self.rotations = 0
        self.obj_to_image = {
            DashObjectType.BLOCK: self.game.block,
            DashObjectType.UP_SPIKE: self.game.up_spike,
            DashObjectType.RIGHT_SPIKE: self.game.right_spike,
            DashObjectType.DOWN_SPIKE: self.game.down_spike,
            DashObjectType.LEFT_SPIKE: self.game.left_spike,
            DashObjectType.YELLOW_ORB: self.game.yellow_orb,
            DashObjectType.PINK_ORB: self.game.pink_orb,
            DashObjectType.BLUE_ORB: self.game.blue_orb,
            DashObjectType.GREEN_ORB: self.game.green_orb,
            DashObjectType.RED_ORB: self.game.red_orb,
            DashObjectType.BLACK_ORB: self.game.black_orb
        }


    @staticmethod
    def add_positions(*positions: tuple[float, float]) -> tuple[float, float]:
        zipped = zip(positions)
        return sum(zipped[0]), sum(zipped[1])


    def find_anchor_position(self, position: tuple[float, float], moves_horizontally: bool) -> tuple[float, float]:
        line = self.game.physics.line if moves_horizontally else 0

        x = (position[0] - line) * self.game.BLOCK_SIZE[0]
        y = self.game.SCREEN_DIMS[1] - position[1] * self.game.BLOCK_SIZE[1] - 189
        return x, y


    def place_object_image(self, image, position: tuple[float, float]) -> None:
        anchor_pos = self.find_anchor_position(position, moves_horizontally=True)
        self.game.screen.blit(image, anchor_pos)


    def place_cube_image(self, position: tuple[float, float]) -> None:
        anchor_pos = self.find_anchor_position(position, moves_horizontally=False)
        cube_image = self.rotated_cubes_images[self.rotations]
        self.game.screen.blit(cube_image, anchor_pos)
        self.rotations += self.ROTATE_SPEED
        self.rotations %= 360


    def render(self) -> None:
        if len(self.game.layout.objects) == 0 or self.game.layout.objects[-1].position[0] - self.game.physics.line <= 0:
            self.game.state = self.game.WON

        if not self.game.physics.falling:
            self.rotations = round(self.rotations / 90) * 90
            self.rotations %= 360

        self.game.screen.blit(self.game.background, (0, 0))
        for obj in self.game.layout.objects:
            if not DashLayout.should_display_object(obj, 0):
                break

            obj_image = self.obj_to_image[obj.objectType]
            self.place_object_image(obj_image, obj.position)

        self.place_cube_image(self.game.physics.cube_position)