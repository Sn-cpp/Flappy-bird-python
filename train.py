import pygame, random, time
from pygame.locals import *
import numpy as np

#VARIABLES
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 20
GRAVITY = 2.5
GAME_SPEED = 15

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT= 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP = 150

bird_rect = pygame.image.load('assets/sprites/bluebird-upflap.png').get_rect()
pipe_rect = pygame.image.load('assets/sprites/pipe-green.png').get_rect()


def generate_bird(n_instance):
    bird_left = np.ones(shape=(n_instance), dtype=np.float32) * (SCREEN_WIDTH / 6)
    bird_right = bird_left + bird_rect.width
    bird_top = np.ones(shape=(n_instance), dtype=np.float32) * (SCREEN_HEIGHT / 2)

    bird_speed = np.ones(shape=(n_instance), dtype=np.float32) * SPEED

    return bird_left, bird_top, bird_right, bird_speed


def generate_pipe(x_pos, n_instance):
    pipe_left = np.ones(shape=(n_instance)) * x_pos
    
    lower_pipe_top = SCREEN_HEIGHT - np.random.randint(100, 300, size=(n_instance))
    lower_pipe_bottom = lower_pipe_top + PIPE_HEIGHT

    upper_pipe_bottom = lower_pipe_top - PIPE_GAP
    upper_pipe_top = upper_pipe_bottom - PIPE_HEIGHT

    return pipe_left, (lower_pipe_top, lower_pipe_bottom), (upper_pipe_top, upper_pipe_bottom) 

def check_collision(
        bird_left, bird_top, bird_right, bird_bottom,
        pipe_left, pipe_top, pipe_right, pipe_bottom
    ):
    
    collisions = (bird_left < pipe_right) & \
                 (bird_right > pipe_left) & \
                 (bird_top < pipe_bottom) & \
                 (bird_bottom > pipe_top)
    
    return collisions

def train():
    n_instance = 1
    
    bird_left, bird_top, bird_right, bird_speed = generate_bird(n_instance)
    pipe_left, (lower_pipe_top, lower_pipe_bottom), (upper_pipe_top, upper_pipe_bottom) = generate_pipe(100, n_instance)
    ground_top = SCREEN_HEIGHT - GROUND_HEIGHT

    is_dead = np.zeros(shape=(n_instance), dtype=np.bool)

    while pipe_left > 0:
        print(bird_left, pipe_left)

        ### TODO: Model outputs as a 1d one-hot array of size (n_instance, 1) describing action:
        # 1: bump
        # 0: do nothing
        model_choice = np.zeros(shape=(n_instance), dtype=np.bool)
        ###

        # State update
        bird_speed = (~model_choice)*bird_speed + model_choice*(-SPEED) + GRAVITY
        bird_top += bird_speed
        bird_bottom = bird_top + bird_rect.height
        
        pipe_left -= GAME_SPEED
        pipe_right = pipe_left + PIPE_WIDTH



        #-------------------------COLLISION CHECK----------------------

        lower_pipe_collision = check_collision(
            bird_left, bird_top, bird_right, bird_bottom,
            pipe_left, lower_pipe_top, pipe_right, lower_pipe_bottom
        )

        upper_pipe_collision = check_collision(
            bird_left, bird_top, bird_right, bird_bottom,
            pipe_left, upper_pipe_top, pipe_right, upper_pipe_bottom
        )

        ground_collision = bird_bottom > ground_top

        print(lower_pipe_collision, upper_pipe_collision, ground_collision)        

        is_dead = (lower_pipe_collision | upper_pipe_collision | ground_collision) 

if __name__ == "__main__":
    train()

# wing = 'assets/audio/wing.wav'
# hit = 'assets/audio/hit.wav'

# pygame.mixer.init()
# pygame.init()
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption('Flappy Bird')

# class Bird(pygame.sprite.Sprite):
#     sprites = [pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha(),
#                         pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha(),
#                         pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha()]
    
#     def __init__(self):
#         pygame.sprite.Sprite.__init__(self)

#         self.images = Bird.sprites 
#         self.image = Bird.sprites[0]

#         self.speed = SPEED

#         self.current_image = 0
#         self.mask = pygame.mask.from_surface(self.image)

#         self.rect = self.image.get_rect()
#         self.rect[0] = SCREEN_WIDTH / 6
#         self.rect[1] = SCREEN_HEIGHT / 2

#     def update(self):
#         self.current_image = (self.current_image + 1) % 3
#         self.image = self.images[self.current_image]
#         self.speed += GRAVITY

#         #UPDATE HEIGHT
#         self.rect[1] += self.speed

#     def bump(self):
#         self.speed = -SPEED

#     def begin(self):
#         self.current_image = (self.current_image + 1) % 3
#         self.image = self.images[self.current_image]

# class Pipe(pygame.sprite.Sprite):
#     sprites = pygame.transform.scale(
#         pygame.image.load('assets/sprites/pipe-green.png').convert_alpha(),
#         (PIPE_WIDTH, PIPE_HEIGHT)
#     )

#     def __init__(self, inverted, xpos, ysize):
#         pygame.sprite.Sprite.__init__(self)

#         self.image = Pipe.sprites

#         self.rect = self.image.get_rect()
#         self.rect[0] = xpos

#         if inverted:
#             self.image = pygame.transform.flip(self.image, False, True)
#             self.rect[1] = - (self.rect[3] - ysize)
#         else:
#             self.rect[1] = SCREEN_HEIGHT - ysize


#         self.mask = pygame.mask.from_surface(self.image)


#     def update(self):
#         self.rect[0] -= GAME_SPEED

# class Ground(pygame.sprite.Sprite):
#     sprites = pygame.transform.scale(
#         pygame.image.load('assets/sprites/base.png').convert_alpha(),
#         (GROUND_WIDTH, GROUND_HEIGHT)
#     )

#     def __init__(self, xpos):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = Ground.sprites

#         self.mask = pygame.mask.from_surface(self.image)

#         self.rect = self.image.get_rect()
#         self.rect[0] = xpos
#         self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT
#     def update(self):
#         self.rect[0] -= GAME_SPEED

# def is_off_screen(sprite):
#     return sprite.rect[0] < -(sprite.rect[2])

# def get_random_pipes(xpos):
#     size = random.randint(100, 300)
#     pipe = Pipe(False, xpos, size)
#     pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
#     return pipe, pipe_inverted

# BACKGROUND = pygame.image.load('assets/sprites/background-day.png')
# BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
# BEGIN_IMAGE = pygame.image.load('assets/sprites/message.png').convert_alpha()

# bird_group = pygame.sprite.Group()
# bird = Bird()
# bird_group.add(bird)

# ground_group = pygame.sprite.Group()

# for i in range (2):
#     ground = Ground(GROUND_WIDTH * i)
#     ground_group.add(ground)

# pipe_group = pygame.sprite.Group()
# for i in range (2):
#     pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
#     pipe_group.add(pipes[0])
#     pipe_group.add(pipes[1])


# FPS = 20
# clock = pygame.time.Clock()

# begin = True

# while begin:

#     clock.tick(FPS) 

#     for event in pygame.event.get():
#         if event.type == QUIT:
#             pygame.quit()
#         if event.type == KEYDOWN:
#             if event.key == K_SPACE or event.key == K_UP:
#                 bird.bump()
#                 pygame.mixer.music.load(wing)
#                 pygame.mixer.music.play()
#                 begin = False

#     screen.blit(BACKGROUND, (0, 0))
#     screen.blit(BEGIN_IMAGE, (120, 150))

#     if is_off_screen(ground_group.sprites()[0]):
#         ground_group.remove(ground_group.sprites()[0])

#         new_ground = Ground(GROUND_WIDTH - 20)
#         ground_group.add(new_ground)

#     bird.begin()
#     ground_group.update()

#     bird_group.draw(screen)
#     ground_group.draw(screen)

#     pygame.display.update()


# pipes_list = pipe_group.sprites()


# def get_object_coords():
#     """API function to get the coordination of the bird and all visible pipes"""
#     bird_coord = np.array([bird.rect[0], bird.rect[1]])
#     pipes_coord = np.array([[pipe.rect[0], pipe.rect[1]] for pipe in pipes_list])

#     return bird_coord, pipes_coord



# while True:
#     clock.tick(FPS)

#     for event in pygame.event.get():
#         if event.type == QUIT:
#             pygame.quit()
#         if event.type == KEYDOWN:
#             if event.key == K_SPACE or event.key == K_UP:
#                 bird.bump()
#                 pygame.mixer.music.load(wing)
#                 pygame.mixer.music.play()

#     screen.blit(BACKGROUND, (0, 0))

#     if is_off_screen(ground_group.sprites()[0]):
#         ground_group.remove(ground_group.sprites()[0])

#         new_ground = Ground(GROUND_WIDTH - 20)
#         ground_group.add(new_ground)

#     if is_off_screen(pipe_group.sprites()[0]):
#         pipe_group.remove(pipe_group.sprites()[0])
#         pipe_group.remove(pipe_group.sprites()[0])

#         pipes = get_random_pipes(SCREEN_WIDTH * 2)

#         pipe_group.add(pipes[0])
#         pipe_group.add(pipes[1])
#         pipes_list = pipe_group.sprites()

#     bird_group.update()
#     ground_group.update()
#     pipe_group.update()

#     bird_group.draw(screen)
#     pipe_group.draw(screen)
#     ground_group.draw(screen)

#     pygame.display.update()

#     if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
#             pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
#         pygame.mixer.music.load(hit)
#         pygame.mixer.music.play()
#         time.sleep(1)
#         break

