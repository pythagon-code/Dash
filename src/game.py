import pygame

from renderer import DashRenderer
from layout_creator import DashLayoutCreator
from physics import DashPhysics


class DashGame:
    SCREEN_DIMS = 960, 600
    BLOCK_SIZE = 36, 36
    ORB_SIZE = 40, 40

    JUST_JUMP_FRAMES = 20


    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode(DashGame.SCREEN_DIMS)
        self.background = pygame.image.load("assets/dash-background.png")
        pygame.display.set_caption("Dash")

        self.clock = clock = pygame.time.Clock()

        self.cube = pygame.transform.scale(pygame.image.load("assets/cube.png"), self.BLOCK_SIZE)
        self.block = pygame.transform.scale(pygame.image.load("assets/block4.png"), self.BLOCK_SIZE)
        self.spike = pygame.transform.scale(pygame.image.load("assets/spike2.png"), self.BLOCK_SIZE)
        self.upside_down_spike = pygame.transform.rotate(self.spike, 180)
        self.yellow_orb = pygame.transform.scale(pygame.image.load("assets/yellow-orb.png"), self.ORB_SIZE)
        self.pink_orb = pygame.transform.scale(pygame.image.load("assets/pink-orb.png"), self.ORB_SIZE)
        self.blue_orb = pygame.transform.scale(pygame.image.load("assets/blue-orb.png"), self.ORB_SIZE)
        self.green_orb = pygame.transform.scale(pygame.image.load("assets/green-orb.png"), self.ORB_SIZE)
        self.red_orb = pygame.transform.scale(pygame.image.load("assets/red-orb.png"), self.ORB_SIZE)
        self.black_orb = pygame.transform.scale(pygame.image.load("assets/black-orb.png"), self.ORB_SIZE)

        self.just_jump = 0

        self.layout = DashLayoutCreator.create_default_layout()
        self.physics = DashPhysics(self.layout)
        self.renderer = DashRenderer(self)


    def loop(self) -> None:
        jump = pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]
        restart = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.just_jump = self.JUST_JUMP_FRAMES
                if event.key == pygame.K_r or event.key == pygame.K_RETURN:
                    restart = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 0:
                    self.just_jump = self.JUST_JUMP_FRAMES

        self.just_jump -= 1

        self.physics.step(jump, self.just_jump > 0, restart)
        self.renderer.render()

        if self.physics.died:
            self.physics = DashPhysics(self.layout)


    def run(self) -> None:
        while True:
            self.loop()
            pygame.display.flip()
            self.clock.tick(120)
