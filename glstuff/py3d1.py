#py3d1.py

#A port of the classical pyode double pendulum example, scripted
#to work with the onpenGL pyggel library.

#The key to using a 3D engine, is to let it do all the hard work and
#calculations, and then tie it back to your own 3D items.

import sys
import pyggel
from pyggel import *
import ode

#initialize pygel screen
pyggel.init(screen_size=(640,480))

#create pygel scene
scene = pyggel.scene.Scene()

#create a pygel light
light = pyggel.light.Light((0,100,0),#so this is aobve most the elements
                          (0.5,0.5,0.5,1),#ambient color
                          (1,1,1,1),#diffuse color
                          (50,50,50,10),#specular
                          (0,0,0),#spot position - not used
                          True) #directional, not a spot light
scene.add_light(light)

#create a pygel camera
camera = pyggel.camera.LookAtCamera((0,1,0),distance=5)

# Create a pyode world object
world = ode.World()
world.setGravity((0,-9.81,0))

# Create two pyode bodies
body1 = ode.Body(world)
M = ode.Mass()
M.setSphere(2500, 0.05)
body1.setMass(M)
body1.setPosition((1,2,0))

body2 = ode.Body(world)
M = ode.Mass()
#M.setSphere(2500, 0.05)
M.setBox(2500,0.1,0.2,0.3)
body2.setMass(M)
body2.setPosition((1,0,0))

# Connect body1 with the static environment
j1 = ode.BallJoint(world)
j1.attach(body1, ode.environment)
j1.setAnchor( (0,2,0) )

# Connect body2 with body1
j2 = ode.BallJoint(world)
j2.attach(body1, body2)
j2.setAnchor( (1,2,0) )


#setup pygel event handler
event_handler = pyggel.event.Handler()

#setup pygel objects.. 
tex = pyggel.data.Texture("texture1.png")
#place spheres anywhere, pyode calculates final positons
s1 = pyggel.geometry.Cube(.5, pos=(0, 0, 0), texture=tex)
s2 = pyggel.geometry.Sphere(0.2, pos=(0, 1, 0), texture=tex)
#add objects to pygel scene
scene.add_3d((s1,s2))

#create a few small pygel balls to represent chain links
"""Instead of using a stretched cube object, and then changing its angle between
   the balls, using a list of spheres for c chain link makes for an
   intereting variation of this pyode sample"""
links1 = 15
chain1=[]
for c in range(links1):
    chain1.append(pyggel.geometry.Sphere(0.05, pos=(0, 0, 0), texture=tex))
    scene.add_3d((chain1[c]))

links2 = 15
chain2=[]
for c in range(links2):
    chain2.append(pyggel.geometry.Sphere(0.05, pos=(0, 0, 0), texture=tex))
    scene.add_3d((chain2[c]))


#setup work variables
fps = 55
dt = 1.0/fps
loopFlag = True
clock = pygame.time.Clock()

#main loop

while 1:

    #update window title
    pyggel.view.set_title("FPS: %s"%int(clock.get_fps()))

    #get events!
    event_handler.update() 

    if event_handler.quit or K_ESCAPE in event_handler.keyboard.hit: #were the quit 'X' box on the window or teh ESCAPE key hit?
        pyggel.quit()
        sys.exit(0)
        

    #clear screen for new drawing...
    pyggel.view.clear_screen()

    # get pyode body positions
    x1,y1,z1 = body1.getPosition()
    x2,y2,z2 = body2.getPosition()

    #update pygel object co-ords with pyode body values
    s1.pos = (x1,y1,z1)
    s2.pos = (x2,y2,z2)

    #manually update the pendulum chain
    for c in range(links1):
        chain1[c].pos =(x1+(x2-x1)/links1*(c+1),y1-(y1-y2)/links1*(c+1),z1)

    #set new links for top chain
    x2=x1
    y2=y1
    z2=z1
    x1=0
    y1=2
    z1=0
    for c in range(links2):
        chain2[c].pos =(x1+(x2-x1)/links2*(c+1),y1-(y1-y2)/links2*(c+1),z1)
 
    #render the scene NOTE to pass the camera parameter
    scene.render(camera) 
    
    #flip the display buffer
    pyggel.view.refresh_screen()


    # Next simulation step
    world.step(dt)

    #limit FPS
    clock.tick(fps)


