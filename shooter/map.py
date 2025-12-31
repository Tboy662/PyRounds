import pygame
import sys

# ------------------
# Initialization
# ------------------
pygame.init()

WIDTH, HEIGHT = 2160, 1080
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Base")
display = True
CLOCK = pygame.time.Clock()
FPS = 60
type="0"
plat=[]
plat.append(pygame.Rect(121,949,200, 20))
plat.append(pygame.Rect(1746,949,200, 20))
plat.append(pygame.Rect(478,828,500, 20))
plat.append(pygame.Rect(1071,828,500, 20))
plat.append(pygame.Rect(295,1024,1500, 20))
plat.append(pygame.Rect(295,580,1500, 20))
plat.append(pygame.Rect(295,800,300, 20))
plat.append(pygame.Rect(1554,800,300, 20))
plat.append(pygame.Rect(911,800,300, 20))
# ------------------
# Colors
# ------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
# ------------------
# Game Variables
# ------------------
running = True
rectangles = []  # store all rectangles

# ------------------
# Main Game Loop
# ------------------
while running:
    CLOCK.tick(FPS)
    # ---- Events ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos,type)
            if type == "0":
                rect = pygame.Rect(event.pos[0], event.pos[1], 200, 20)
                rectangles.append(rect)
            if type == "1":
                rect = pygame.Rect(event.pos[0], event.pos[1], 300, 20)
                rectangles.append(rect)
            if type == "2":
                rect = pygame.Rect(event.pos[0], event.pos[1], 500, 20)
                rectangles.append(rect)
            if type == "3":
                rect = pygame.Rect(event.pos[0], event.pos[1], 1500, 20)
                rectangles.append(rect)
            if type == "4":
                rect = pygame.Rect(event.pos[0], event.pos[1], 200, 300)
                rectangles.append(rect)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                type = "0"
            if event.key == pygame.K_1:
                type = "1"
            if event.key == pygame.K_2:
                type = "2"
            if event.key == pygame.K_3:
                type = "3"
            if event.key == pygame.K_4:
                type = "4"
            

    # ---- Draw ----
    SCREEN.fill(BLACK)

    for rect in rectangles:
        pygame.draw.rect(SCREEN, WHITE, rect)
    for rect in plat:
        if display == True:
            pygame.draw.rect(SCREEN, RED, rect)

    pygame.display.flip()

# ---
