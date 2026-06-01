from pygame.sprite import Sprite, Group, groupcollide, collide_mask
from pygame import image, mask, transform
import numpy as np


from settings import *

class PyGamePipe(Sprite):
    pipe_sprites = None

    @staticmethod
    def load_sprite():
        PyGamePipe.pipe_sprites = transform.scale(
            image.load('assets/sprites/pipe-green.png').convert_alpha(),
            (PIPE_WIDTH, PIPE_HEIGHT)
        )

    def __init__(self, inverted, left, top):
        Sprite.__init__(self)

        self.image = PyGamePipe.pipe_sprites

        self.rect = self.image.get_rect()
        self.rect[0] = left
        self.rect[1] = top

        if inverted:
            self.image = transform.flip(self.image, False, True)

        self.mask = mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED



class PyGamePipeGroup:
    def __init__(self, seed: int = 42):
        self.rng = np.random.default_rng(seed=seed)
        self.pipes = Group()
        self.pipe_rect = PyGamePipe.pipe_sprites.get_rect()

        self.generate_pipe()

    def generate_pipe(self, x_pos: int = 800):
        size = self.rng.integers(low=100, high=300)

        # lower pipe
        self.pipes.add(PyGamePipe(False, x_pos, SCREEN_HEIGHT - size))
        
        # upper pipe
        self.pipes.add(PyGamePipe(True, x_pos, SCREEN_HEIGHT - size - PIPE_GAP - self.pipe_rect[3]))

    def update(self):
        self.pipes.update()

    def regen_pipe(self, x_pos):
        pipe = self.pipes.sprites()[0]

        if pipe.rect[0] < -(pipe.rect[2]):
            self.pipes.empty()
            self.generate_pipe(x_pos)

    def check_collision(self, bird_group: Group):
        return groupcollide(bird_group, self.pipes, False, False, collide_mask)

    def draw(self, screen):
        self.pipes.draw(screen)

class NumpyPipeGroup:
    def __init__(self, n_instance: int, seed: int = 42):
        self.n_instance = n_instance
        self.rng = np.random.default_rng(seed=seed)
        self.pipe_rect = PyGamePipe.pipe_sprites.get_rect()

        self.generate_pipe()

    def generate_pipe(self, x_pos: int = 800):
        self.pipe_left = np.ones(shape=(self.n_instance)) * x_pos
        self.pipe_right = self.pipe_left + PIPE_WIDTH
        
        self.lower_pipe_top = SCREEN_HEIGHT - np.random.randint(100, 300, size=(self.n_instance))
        self.lower_pipe_bottom = self.lower_pipe_top + PIPE_HEIGHT

        self.upper_pipe_bottom = self.lower_pipe_top - PIPE_GAP
        self.upper_pipe_top = self.upper_pipe_bottom - PIPE_HEIGHT

    def update(self):
        self.pipe_left -= GAME_SPEED
        self.pipe_right = self.pipe_left + PIPE_WIDTH

    def regen_pipe(self, x_pos):
        if np.all(self.pipe_left < -self.pipe_rect[2]):
            self.generate_pipe(x_pos)

    def is_off_screen(self):
        return 

    def check_collision(self, bird_left: np.ndarray, bird_top: np.ndarray, bird_right: np.ndarray, bird_bottom: np.ndarray):
        upper_pipe_collision = self._pipe_collide(
            bird_left, bird_top, bird_right, bird_bottom,
            self.pipe_left, self.upper_pipe_top, self.pipe_right, self.upper_pipe_bottom
        )

        lower_pipe_collision = self._pipe_collide(
            bird_left, bird_top, bird_right, bird_bottom,
            self.pipe_left, self.lower_pipe_top, self.pipe_right, self.lower_pipe_bottom
        )

        return upper_pipe_collision | lower_pipe_collision
    
    def _pipe_collide(self,
        bird_left: np.ndarray, bird_top: np.ndarray, bird_right: np.ndarray, bird_bottom: np.ndarray,
        pipe_left: np.ndarray, pipe_top: np.ndarray, pipe_right: np.ndarray, pipe_bottom: np.ndarray
    ):
    
        collisions = (bird_left < pipe_right) & \
                    (bird_right > pipe_left) & \
                    (bird_top < pipe_bottom) & \
                    (bird_bottom > pipe_top)
    
        return collisions