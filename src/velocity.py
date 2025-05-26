class DashVelocity:
    MAX_SPEED = 0.4
    GRAVITY = 0.01


    def __init__(self) -> None:
        self.velocity = 0
        self.reversed_gravity = False


    def clamp_speed(self) -> None:
        self.velocity = max(-DashVelocity.MAX_SPEED, min(DashVelocity.MAX_SPEED, self.velocity))


    def fall(self) -> None:
        self.velocity += self.GRAVITY if self.reversed_gravity else -self.GRAVITY
        self.clamp_speed()


    def set_speed(self, speed: float) -> None:
        self.velocity = -speed if self.reversed_gravity else speed
        self.clamp_speed()


    def reverse_gravity(self) -> None:
        self.reversed_gravity = not self.reversed_gravity
        self.velocity = 0
