import argparse
import pygame, random, time
from pygame.locals import *
import numpy as np
from pygame import image, transform

from entites.bird import *
from entites.pipe import *
from entites.ground import *

from settings import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--mode", type=str, default="user", help="Running mode")

    args = parser.parse_args()

    allowed_mode = ["user", "model_ui", "model_cli"]
    assert args.mode in allowed_mode, "Unknown mode" 

    if args.mode == "model_cli":
        bird_group = NumpyBirdGroup()
        pipe_group = NumpyPipeGroup()
        ground_group = NumpyGroundGroup()

        clock = None
    else:
        pygame.mixer.init()
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Flappy Bird')

        BACKGROUND = image.load('assets/sprites/background-day.png')
        BACKGROUND = transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
        BEGIN_IMAGE = image.load('assets/sprites/message.png').convert_alpha()

        PyGameBird.load_sprites()
        PyGameGround.load_sprite()
        PyGamePipe.load_sprite()

        bird_group = PyGameBirdGroup()
        pipe_group = PyGamePipeGroup()
        ground_group = PyGameGroundGroup()

        clock = pygame.time.Clock()
        begin = True
        if args.mode == "user":
            while begin:
                clock.tick(FPS)
                
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                    if event.type == KEYDOWN:
                        if event.key == K_SPACE or event.key == K_UP:
                            bird_group.bump()
                            pygame.mixer.music.load(wing)
                            pygame.mixer.music.play()
                            begin = False

                screen.blit(BACKGROUND, (0, 0))
                screen.blit(BEGIN_IMAGE, (120, 150))

                ground_group.regen_ground(GROUND_WIDTH - 20)

                bird_group.begin()
                ground_group.update()

                bird_group.draw(screen)
                ground_group.draw(screen)

                pygame.display.update()

            while True:
                clock.tick(FPS)

                bird_low = bird_group.bird.rect.bottom

                if bird_low > 400:
                    bird_group.bump()

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                    if event.type == KEYDOWN:
                        if event.key == K_SPACE or event.key == K_UP:
                            bird_group.bump()
                            pygame.mixer.music.load(wing)
                            pygame.mixer.music.play()

                screen.blit(BACKGROUND, (0, 0))

                ground_group.regen_ground(GROUND_WIDTH - 20)
                pipe_group.regen_pipe(SCREEN_WIDTH)

                bird_group.update()
                ground_group.update()
                pipe_group.update()

                bird_group.draw(screen)
                pipe_group.draw(screen)
                ground_group.draw(screen)

                pygame.display.update()

                if ground_group.check_collision(bird_group.birds) or pipe_group.check_collision(bird_group.birds):
                    pygame.mixer.music.load(hit)
                    pygame.mixer.music.play()
                    time.sleep(1)
                    break
        