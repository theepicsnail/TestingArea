import pygame, sys
from pygame.locals import *
from math import *
pygame.init()
fpsClock = pygame.time.Clock()

window = pygame.display.set_mode((640,480))
pygame.display.set_caption("Pygame sample.")


black=pygame.Color(  0,  0,  0)
white=pygame.Color(255,255,255)

size = 40

board = [[0 for i in range(10)] for j in range(10)]
def toggle(r,c):
    global board
    if r<0 or c<0 or r>=len(board) or c>=len(board[0]):
        return
    print "G"
    board[r][c]=not board[r][c]
    
def click(r,c):
    global board
    if r<0 or c<0 or r>=len(board) or c>=len(board[0]):
        return
    print "G"
    toggle(r,c-1)
    toggle(r,c+1)
    toggle(r,c-2)
    toggle(r,c+2)
    toggle(r,c)
    toggle(r-1,c)
    toggle(r+1,c)
    toggle(r-2,c)
    toggle(r+2,c)
    
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
                pygame.quit()
                sys.exit()      
        if event.type == MOUSEBUTTONDOWN:
            mx,my = event.pos
            click(mx/size,my/size)
    pygame.display.update()
    fpsClock.tick(30)

    window.fill(white)

    for r,row in enumerate(board):
        for c,val in enumerate(row):            
            pygame.draw.rect(window,black,(r*size+2,c*size+2,size-4,size-4))
            if val:
                pygame.draw.rect(window,white,(r*size+4,c*size+4,size-8,size-8))
                
                
                
                