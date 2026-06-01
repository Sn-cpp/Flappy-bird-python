from pygame.sprite import Sprite, Group, groupcollide, collide_mask
from pygame import image, mask, transform
import numpy as np


from settings import *

class PyGameGround(Sprite):
    ground_sprites = None

    @staticmethod
    def load_sprite():
        PyGameGround.ground_sprites = transform.scale(
        image.load('assets/sprites/base.png').convert_alpha(),
        (GROUND_WIDTH, GROUND_HEIGHT)
    )

    def __init__(self, xpos):
        Sprite.__init__(self)
        self.image = PyGameGround.ground_sprites
        self.mask = mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        self.rect[0] -= GAME_SPEED



class PyGameGroundGroup:
    def __init__(self):
        self.ground = Group()
        self.generate_ground(0)
        self.generate_ground(GROUND_WIDTH)

    def update(self):
        self.ground.update()

    def check_collision(self, bird_group: Group):
        return groupcollide(bird_group, self.ground, False, False, collide_mask)

    def generate_ground(self, x_pos):
        ground = PyGameGround(x_pos)
        self.ground.add(ground)

    def regen_ground(self, x_pos):
        ground = self.ground.sprites()[0]

        if ground.rect[0] < -(ground.rect[2]):
            self.ground.remove(ground)
            self.generate_ground(x_pos)

    def draw(self, screen):
        self.ground.draw(screen)

class NumpyGroundGroup:
    def __init__(self):
        self.ground_top = SCREEN_HEIGHT - GROUND_HEIGHT
        pass

    def check_collision(self, bird_bottom: np.ndarray):
        return bird_bottom > self.ground_top

