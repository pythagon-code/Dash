from layout import *


class DashRenderer:
    def __init__(self, game) -> None:
        from game import DashGame       # Prevent circular import
        self.game: DashGame = game
        self.obj_to_image = {
            DashObjectType.BLOCK: self.game.block,
            DashObjectType.SPIKE: self.game.spike,
            DashObjectType.UPSIDE_DOWN_SPIKE: self.game.upside_down_spike,
            DashObjectType.YELLOW_ORB: self.game.yellow_orb,
            DashObjectType.PINK_ORB: self.game.pink_orb,
            DashObjectType.BLUE_ORB: self.game.blue_orb,
            DashObjectType.RED_ORB: self.game.red_orb
        }


    @staticmethod
    def add_positions(*positions: tuple[int, int]) -> tuple[int, int]:
        zipped = zip(positions)
        return sum(zipped[0]), sum(zipped[1])


    def find_anchor_position(self, position: tuple[int, int], moves_horizontally: bool) -> tuple[int, int]:
        line = self.game.physics.line if moves_horizontally else 0

        x = (position[0] - line) * self.game.BLOCK_SIZE[0]
        y = self.game.SCREEN_DIMS[1] - position[1] * self.game.BLOCK_SIZE[1] - 189
        return x, y


    def place_object_image(self, image, position: tuple[int, int], moves_horizontally: bool=True) -> None:
        anchor_pos = self.find_anchor_position(position, moves_horizontally)
        self.game.screen.blit(image, anchor_pos)


    def render(self) -> None:
        self.game.screen.blit(self.game.background, (0, 0))
        for obj in self.game.layout.objects:
            if not DashLayout.should_display_object(obj, 0):
                break

            obj_image = self.obj_to_image[obj.objectType]
            self.place_object_image(obj_image, obj.position)

        self.place_object_image(self.game.cube, self.game.physics.cube_position, False)