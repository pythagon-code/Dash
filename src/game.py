import pygame

from src.renderer import DashRenderer
from src.layout_reader import DashLayoutReader
from src.physics import DashPhysics


class DashGame:
    SCREEN_DIMS = 960, 600
    BLOCK_SIZE = 36, 36
    ORB_SIZE = 40, 40

    JUST_JUMP_FRAMES = 20

    NOT_STARTED = 0
    RUNNING = 1
    WON = 2


    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode(DashGame.SCREEN_DIMS)
        self.background = pygame.image.load("assets/dash-background.png")
        pygame.display.set_caption("Dash")
        pygame.display.set_icon(pygame.image.load("assets/spike.png"))  

        self.menu = pygame.image.load("assets/dash-menu.png")
        self.win_screen = pygame.image.load("assets/dash-win-screen.png")

        self.clock = clock = pygame.time.Clock()

        self.cube = pygame.transform.scale(pygame.image.load("assets/cube.png"), self.BLOCK_SIZE)
        self.block = pygame.transform.scale(pygame.image.load("assets/block4.png"), self.BLOCK_SIZE)
        self.up_spike = pygame.transform.scale(pygame.image.load("assets/spike2.png"), self.BLOCK_SIZE)
        self.right_spike = pygame.transform.rotate(self.up_spike, -90)
        self.down_spike = pygame.transform.rotate(self.up_spike, 180)
        self.left_spike = pygame.transform.rotate(self.up_spike, 90)
        self.yellow_orb = pygame.transform.scale(pygame.image.load("assets/yellow-orb.png"), self.ORB_SIZE)
        self.pink_orb = pygame.transform.scale(pygame.image.load("assets/pink-orb.png"), self.ORB_SIZE)
        self.blue_orb = pygame.transform.scale(pygame.image.load("assets/blue-orb.png"), self.ORB_SIZE)
        self.green_orb = pygame.transform.scale(pygame.image.load("assets/green-orb.png"), self.ORB_SIZE)
        self.red_orb = pygame.transform.scale(pygame.image.load("assets/red-orb.png"), self.ORB_SIZE)
        self.black_orb = pygame.transform.scale(pygame.image.load("assets/black-orb.png"), self.ORB_SIZE)

        self.state = self.NOT_STARTED
        self.just_jump = 0

        self.layout = DashLayoutReader.read_layout_from_csv("layouts/level1.csv")
        self.physics = DashPhysics(self.layout)
        self.renderer = DashRenderer(self)


    def set_layout(self, event: pygame.event.EventType):
        assert event.type == pygame.KEYDOWN
        if event.key == pygame.K_1:
            self.layout = DashLayoutReader.read_layout_from_csv("layouts/level1.csv")
        elif event.key == pygame.K_2:
            self.layout = DashLayoutReader.read_layout_from_csv("layouts/level2.csv")
        elif event.key == pygame.K_3:
            self.layout = DashLayoutReader.read_layout_from_csv("layouts/level3.csv")
        elif event.key == pygame.K_4:
            self.layout = DashLayoutReader.read_layout_from_csv("layouts/level4.csv")
        elif event.key == pygame.K_5:
            self.layout = DashLayoutReader.read_layout_from_csv("layouts/level5.csv")
        elif event.key == pygame.K_6:
            self.layout = DashLayoutReader.read_layout_from_csv("layouts/level6.csv")
        else:
            return

        self.state = self.RUNNING
        self.physics = DashPhysics(self.layout)

    def loop(self) -> None:
        if self.state != self.RUNNING:
            if self.state == self.NOT_STARTED:
                self.screen.blit(self.menu, (0, 0))
            elif self.state == self.WON:
                self.screen.blit(self.win_screen, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.set_layout(event)
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            return

        jump = pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.just_jump = self.JUST_JUMP_FRAMES

                self.set_layout(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 0:
                    self.just_jump = self.JUST_JUMP_FRAMES

        self.just_jump -= 1

        self.physics.step(jump, self.just_jump > 0)
        self.renderer.render()

        if self.physics.died:
            self.physics = DashPhysics(self.layout)


    def run(self) -> None:
        while True:
            self.loop()
            pygame.display.flip()
            self.clock.tick(120)
