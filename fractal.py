import pygame
import random
import cmath
import math

pygame.init()

WIDTH, HEIGHT = 1100, 1100
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((0,0,0))
pygame.display.set_caption("Fractal Generator")

clock = pygame.time.Clock()

Display_WIDTH, Display_HEIGHT = 1024, 1024
Display = pygame.Surface((Display_WIDTH, Display_HEIGHT))
Display_rect = pygame.Rect(50, 50, Display_WIDTH, Display_HEIGHT)
Display.fill((0,0,0))

for x in range(Display_WIDTH):
    for y in range(Display_HEIGHT):
        iteration = 0
        z = complex(0, 0)
        c = complex((x-(Display_WIDTH/2))/(Display_WIDTH/4), (-y+(Display_HEIGHT/2))/(Display_WIDTH/4))
        for i in range(100):
            z = (z*z) + c
            if abs(z) > 2:
                break
            iteration += 1
        Display.set_at((x,y), (int(iteration/100*255), int(iteration/100*255), int(iteration/100*255)))

print("calc done")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.blit(Display, (50, 50))

    pygame.display.flip()

    clock.tick(50)

# Quit pygame window 
pygame.quit()	 
	
