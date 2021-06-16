import pygame
import os
import random

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 480, 640
FPS = 60

# colors
Black = (0, 0, 0)
WHITE = (255, 255, 255)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# fonts
SCORE_FONT = pygame.font.SysFont('comicsans', 100)
GAME_OVER_FONT = pygame.font.SysFont('comicsans', 100)

# IMAGES
BACKGROUND = pygame.image.load(os.path.join('Assets', 'background2.png'))
BIRD = pygame.image.load(os.path.join('Assets', 'flappybird.png'))
GROUND = pygame.image.load(os.path.join('Assets', 'ground.png'))
TOP_PIPE = pygame.image.load(os.path.join('Assets', 'pipe3.png'))
BOTTOM_PIPE = pygame.image.load(os.path.join('Assets', 'pipe2.png'))

# sounds
DEATH_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'die.mp3'))
DEATH_SOUND.set_volume(.25)
WING_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'wing.mp3'))
WING_SOUND.set_volume(.25)
HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'hit.mp3'))
HIT_SOUND.set_volume(.25)
POINT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'point.mp3'))
POINT_SOUND.set_volume(.25)

# events
game_over = pygame.USEREVENT + 1
point = pygame.USEREVENT + 2


def draw_game_over(text):
    draw_text = GAME_OVER_FONT.render(text, True, Black)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(1500)


def handle_pipes(bird, pipes, pipes2):
    for top_pipe in pipes:
        top_pipe.x -= 3
        if top_pipe.x + TOP_PIPE.get_width() < 0:
            pipes.remove(top_pipe)
        if bird.colliderect(top_pipe):
            pygame.event.post(pygame.event.Event(game_over))
            HIT_SOUND.play()
        if top_pipe.x <= bird.x <= top_pipe.x + 2:
            pygame.event.post(pygame.event.Event(point))
            POINT_SOUND.play()
    for bottom_pipe in pipes2:
        bottom_pipe.x -= 3
        if bottom_pipe.x + BOTTOM_PIPE.get_width() < 0:
            pipes2.remove(bottom_pipe)
        if bird.colliderect(bottom_pipe):
            pygame.event.post(pygame.event.Event(game_over))
            HIT_SOUND.play()


def draw_window(bird, score, pipes, pipes2):
    WIN.blit(BACKGROUND, (0, 0))
    score_text = SCORE_FONT.render(str(score), True, WHITE)
    WIN.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, score_text.get_height()))

    WIN.blit(BIRD, (bird.x, bird.y))

    for top_pipe in pipes:
        WIN.blit(TOP_PIPE, (top_pipe.x, top_pipe.y))

    for bottom_pipe in pipes2:
        WIN.blit(BOTTOM_PIPE, (bottom_pipe.x, bottom_pipe.y))
    ground = WIN.blit(GROUND, (0, HEIGHT - GROUND.get_height()))
    if bird.colliderect(ground):
        pygame.event.post(pygame.event.Event(game_over))
        DEATH_SOUND.play()

    pygame.display.update()


def main():
    bird = pygame.Rect(
        WIDTH / 2 - BIRD.get_width() / 2, HEIGHT / 2, BIRD.get_width(), BIRD.get_height())
    clock = pygame.time.Clock()
    run = True
    key_down = False
    flag = False
    score = 0
    count = 0

    pipes = []
    pipes2 = []

    while run:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_SPACE] and not key_down:
                bird.y -= 90
                WING_SOUND.play()
                key_down = True
            elif key_down and not keys_pressed[pygame.K_SPACE]:
                key_down = False
            if event.type == point:
                score += 1
            if event.type == game_over:
                flag = True
                break
        if flag:
            break
        bird.y += 3
        temp = random.randrange(0 - 3 * HEIGHT // 4,
                                HEIGHT - GROUND.get_height() - HEIGHT // 4 - TOP_PIPE.get_height())
        top_pipe = pygame.Rect(WIDTH + count, temp, TOP_PIPE.get_width(), TOP_PIPE.get_height())
        bottom_pipe = pygame.Rect(WIDTH + count, temp + 156 + TOP_PIPE.get_height(),
                                  BOTTOM_PIPE.get_width(), BOTTOM_PIPE.get_height())
        pipes.append(top_pipe)
        pipes2.append(bottom_pipe)

        handle_pipes(bird, pipes, pipes2)
        draw_window(bird, score, pipes, pipes2)

        count += 350
    draw_game_over("Game Over")
    main()


if __name__ == '__main__':
    main()
