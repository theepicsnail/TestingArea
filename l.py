
## <code>
SCREEN_SIZE = (800,600)

light_size = 100
light_location = (200,200)

## Setup
import pygame
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)

## A black mask for the screen.
mask = pygame.surface.Surface(SCREEN_SIZE).convert_alpha()
mask.fill((0,0,0,255))

## An inefficiently-drawn shaded "light"
radius = 200
t = 255
delta = 3
while radius > 50:
        pygame.draw.circle(mask,(0,0,0,t),light_location,radius)
        t -= delta
        radius -= delta
        pygame.draw.circle(mask,(0,0,0,95),light_location,radius)

## A sharp-edged white "light"
pygame.draw.circle(mask,(0,0,0,0),(400,275),50)

## A red-tinted "light"
pygame.draw.circle(mask,(192,0,0,128),(300,375),50)

## A blue screen with a couple of white squares
screen.fill((0,0,255))
pygame.draw.rect(screen,(255,255,255),(100,100,100,100))
pygame.draw.rect(screen,(255,255,255),(300,250,100,100))

## Cover the screen with the partly-translucent mask
screen.blit(mask,(0,0))

## Make it so
pygame.display.update()
## </code>
