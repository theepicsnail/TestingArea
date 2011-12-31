import pygame,sys
import urllib
from pygame.locals import *

def getUrls():
    feed = urllib.urlopen("http://www.reddit.com/r/teen_girls/new/.json?sort=new")
    true,false,null = True,False,None
    json = eval(feed.read())
    urls = [item["data"].get("url","") for item in json["data"]["children"]]
    urls = filter(lambda x:x,urls)
    return urls


pygame.init()
fpsClock = pygame.time.Clock()

window = pygame.display.set_mode((640,480))
pygame.display.set_caption("Pygame sample.")



urls = []
def setImage(url):
    file("tmp.img","w").write(urllib.urlopen(url).read())
    img = pygame.image.load("tmp.img")
    window = pygame.display.set_mode((img.get_width(),img.get_height()))
#    window.fill((255,255,255))
    window.blit(img,(0,0))
    pygame.display.update()


while True:
        
    for event in pygame.event.get():
        if event.type == QUIT:
                pygame.quit()
                sys.exit()    
                
               
    if urls:                    
        setImage(urls[0])
        urls.pop(0)
    else:
        urls = getUrls()
    
    fpsClock.tick(1)





import urllib

import pprint
pprint.pprint(json)




