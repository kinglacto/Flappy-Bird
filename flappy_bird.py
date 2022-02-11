import pygame
import random
import time

FPS = 70
CLOCK = pygame.time.Clock()

WIDTH = 288
HEIGHT = 512

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

BACKGROUND = pygame.image.load("assets/background.png").convert()
BASE = pygame.image.load("assets/base.png").convert()
GAME_OVER_MSG = pygame.image.load("assets/game_over.png").convert_alpha()
START_MSG = pygame.image.load("assets/start_message.png").convert_alpha()
UP_PIPE = pygame.image.load("assets/up_pipe.png").convert_alpha()
DOWN_PIPE = pygame.transform.rotate(UP_PIPE, 180).convert_alpha()
BIRD = [pygame.image.load(f"assets/{state}.png").convert_alpha() for state in ["bird_mid", "bird_up", "bird_mid", "bird_down"]]
NUMBERS = [pygame.image.load(f"assets/{i}.png").convert_alpha() for i in range(10)]

PIPE_WIDTH = UP_PIPE.get_width()
PIPE_GAP = 100
DOWN_PIPE_MAX_HEIGHT = 250
DOWN_PIPE_MIN_HEIGHT = 70
PIPE_SPEED = 2
PIPE_DELAY = 1.2

BIRD_JUMP_SPEED = 9.7
BIRD_SINK_SPEED = 2.5

Y_CORD_PAIRS_FOR_PIPES = []
for _ in range(50):
    down_pipe_y = random.randrange(DOWN_PIPE_MIN_HEIGHT - DOWN_PIPE.get_height(), DOWN_PIPE_MAX_HEIGHT - DOWN_PIPE.get_height(), 10)
    Y_CORD_PAIRS_FOR_PIPES.append((down_pipe_y, down_pipe_y + DOWN_PIPE.get_height() + PIPE_GAP))

def LOAD_SCREEN():
    SCREEN.blit(BACKGROUND, (0, 0))
    SCREEN.blit(BASE, (0, 400))

class PipePair:
    def __init__(self):
        self.x = WIDTH
        self.y_pair = random.choice(Y_CORD_PAIRS_FOR_PIPES)
        self.score = 0

    def blit(self):
        if self.x < (-1 * PIPE_WIDTH):
            self.x = WIDTH
            self.y_pair = random.choice(Y_CORD_PAIRS_FOR_PIPES)
            self.score += 1

        else:
            self.x -= PIPE_SPEED
            SCREEN.blit(DOWN_PIPE, (self.x, self.y_pair[0]))
            SCREEN.blit(UP_PIPE, (self.x, self.y_pair[1]))
            SCREEN.blit(BASE, (0, 400))

class Bird:
    def __init__(self):
        self.x = 40
        self.y = 256
        self.is_jump = False
        self.flap_state = 3
        self.leaps = 0

    def blit(self):
        SCREEN.blit(BIRD[self.flap_state], (self.x, self.y))
        
    def flap(self):
        self.flap_state = 0 if self.flap_state == 3 else self.flap_state + 1
        
    def descend(self):
        if not self.is_jump and self.y < 375:
            self.y += BIRD_SINK_SPEED

    def jump(self):
        if self.is_jump:
            if self.leaps <= 3:
                self.y -= BIRD_JUMP_SPEED
                self.leaps += 1

            else:
                self.leaps = 0
                self.is_jump = False

def update_score(score):
    score = str(score)
    for i in range(len(score)):
        SCREEN.blit(NUMBERS[int(score[i])], (120 + (i * 30), 30))

def iscollision(bird, pipe1, pipe2):
    bird_rect = pygame.Rect(bird.x, bird.y, 34, 24)
    pipe1_rects = pygame.Rect(pipe1.x, pipe1.y_pair[0], 52, 320), pygame.Rect(pipe1.x, pipe1.y_pair[1], 52, 320)
    pipe2_rects = pygame.Rect(pipe2.x, pipe2.y_pair[0], 52, 320), pygame.Rect(pipe2.x, pipe2.y_pair[1], 52, 320)

    if pipe1_rects[0].colliderect(bird_rect) or pipe1_rects[1].colliderect(bird_rect) or pipe2_rects[0].colliderect(bird_rect) or pipe2_rects[1].colliderect(bird_rect):
        return True
    return False

def game():
    bird = Bird()
    pipe1 = PipePair()
    pipe2 = PipePair()

    start_game = is_over = place_second_pipe = False

    score = 0

    LOAD_SCREEN()
    SCREEN.blit(START_MSG, (54, 100))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP):
                if not start_game:
                    start_game = True
                    start_time = time.time()
                    CLOCK.tick()

                if not is_over:
                    bird.is_jump = True
                    bird.leaps = 0

                else:
                    return None

        if not is_over and start_game:
            LOAD_SCREEN()

            bird.flap()
            bird.jump()
            bird.descend()
            bird.blit()

            pipe1.blit()
            if place_second_pipe:
                pipe2.blit()   
            elif time.time() - start_time > PIPE_DELAY:
                place_second_pipe = True

            if bird.x in ((pipe1.x + 52)/2 , (pipe2.x + 52)/2):
                score += 1

            if iscollision(bird, pipe1, pipe2) or score == 1000:
                is_over = True

            update_score(score)

        elif is_over and start_game:
            SCREEN.blit(GAME_OVER_MSG, (53, 100))
            
        CLOCK.tick(FPS)
        pygame.display.update()

def main():
    while True:
        game()

if __name__ == "__main__":
    main()