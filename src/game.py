import pygame

from renderer import DashRenderer
from layout_creator import DashLayoutCreator
from physics import DashPhysics


class DashGame:
    SCREEN_DIMS = 960, 600
    BLOCK_SIZE = 36, 36


    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode(DashGame.SCREEN_DIMS)
        self.background = pygame.image.load("assets/dash-background.png")
        pygame.display.set_caption("Dash")

        self.clock = clock = pygame.time.Clock()

        self.cube = pygame.transform.scale(pygame.image.load("assets/cube.png"), DashGame.BLOCK_SIZE)
        self.block = pygame.transform.scale(pygame.image.load("assets/block4.png"), DashGame.BLOCK_SIZE)
        self.spike = pygame.transform.scale(pygame.image.load("assets/spike2.png"), DashGame.BLOCK_SIZE)
        self.upside_down_spike = pygame.transform.rotate(self.spike, 180)
        self.yellow_orb = pygame.transform.scale(pygame.image.load("assets/yellow-orb.png"), DashGame.BLOCK_SIZE)
        self.pink_orb = pygame.transform.scale(pygame.image.load("assets/pink-orb.png"), DashGame.BLOCK_SIZE)
        self.blue_orb = pygame.transform.scale(pygame.image.load("assets/blue-orb.png"), DashGame.BLOCK_SIZE)
        self.red_orb = pygame.transform.scale(pygame.image.load("assets/red-orb.png"), DashGame.BLOCK_SIZE)

        self.layout = DashLayoutCreator.create_default_layout()
        self.physics = DashPhysics(self.layout)
        self.renderer = DashRenderer(self)


    def loop(self) -> None:
        jump = pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]
        just_jump = False
        restart = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    just_jump = True
                if event.key == pygame.K_r or event.key == pygame.K_RETURN:
                    restart = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 0:
                    just_jump = True

        self.physics.step(jump, just_jump, restart)
        self.renderer.render()

        if self.physics.died:
            self.physics = DashPhysics(self.layout)


    def run(self) -> None:
        while True:
            self.loop()
            pygame.display.flip()
            self.clock.tick(60)
