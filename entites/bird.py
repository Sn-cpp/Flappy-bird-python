from pygame.sprite import Sprite, Group
from pygame import image, mask
import numpy as np


from settings import *



class PyGameBird(Sprite):
    bird_sprites = None

    @staticmethod
    def load_sprites():
        PyGameBird.bird_sprites = [
            image.load('assets/sprites/bluebird-upflap.png').convert_alpha(),
            image.load('assets/sprites/bluebird-midflap.png').convert_alpha(),
            image.load('assets/sprites/bluebird-downflap.png').convert_alpha()
        ]

    def __init__(self):
        Sprite.__init__(self)

        self.images = PyGameBird.bird_sprites

        self.speed = SPEED

        self.current_image = 0
        self.image = self.images[0]
        self.mask = mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH / 6
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        self.speed += GRAVITY

        #UPDATE HEIGHT
        self.rect[1] += self.speed

    def bump(self):
        self.speed = -SPEED

    def begin(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]

class PyGameBirdGroup:
    def __init__(self):
        self.birds = Group()
        self.bird = PyGameBird()
        self.birds.add(self.bird)

    def update(self):
        self.birds.update()

    def bump(self):
        self.bird.bump()

    def begin(self):
        self.bird.begin()

    def draw(self, screen):
        self.birds.draw(screen)

class NumpyBirdGroup:
    def __init__(self, n_instance: int):
        self.n_instance = n_instance

        self.rect = PyGameBird.bird_sprites[0].get_rect()

        self.bird_left = np.ones(shape=(n_instance), dtype=np.float32) * (SCREEN_WIDTH / 6)
        self.bird_right = self.bird_left + self.rect.width
        self.bird_top = np.ones(shape=(n_instance), dtype=np.float32) * (SCREEN_HEIGHT / 2)

        self.speed = np.ones(shape=(n_instance), dtype=np.float32) * SPEED

    def update(self):
        self.speed += GRAVITY

        #UPDATE HEIGHT
        self.bird_top += self.speed

    def bump(self, model_choice: np.ndarray):
        self.speed = (~model_choice)*self.speed + model_choice*(-SPEED)

    def begin(self):
        pass