#!/usr/bin/env python
import pika
import threading

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

#channel.queue_delete(queue="graphics")
#channel.queue_delete(queue="events")


channel.queue_declare(queue='graphics')

print ' [*] Waiting for messages. To exit press CTRL+C'


   
import pygame
from pygame.locals import *
 
  
    
    
class Display:
    color = (255,0,0)
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((500,500),DOUBLEBUF)
        self.screen = pygame.display.get_surface()
    def Clear(self):
        self.screen.fill(self.color)
    def Flip(self):
        pygame.display.flip()
    def Color(self,r,g,b):
        self.color=(r,g,b)
    def Line(self,x,y,x2,y2):
        pygame.draw.line(self.screen,self.color,(x,y),(x2,y2),3)
class EventPublisher(threading.Thread):
    def __init__(self,display):
        self.display = display
        threading.Thread.__init__(self)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange="events",type="fanout")
        self.start()
    def quit(self):
        self.running = False
        print "Closing event channel"
        self.connection.close()
        print "Quit called"
    def run(self):
        self.running = True
        pygame.register_quit(self.quit)
        while self.running:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                self.running = False
            event.dict["type"]=event.type
            self.channel.basic_publish(exchange="events",
                                       routing_key=str(event.type),
                                       body="{}".format(event.dict))
            
            print "S out",event.dict

disp = Display()
EventPublisher(disp)
pygame.register_quit(connection.close)

def callback(ch, method, properties, body):
    global disp
    print "S in",body
    try: 
        eval("disp.{}".format(body)) #... i shouldn't even test with this in...
    except:
        print "Exception."
        pass
 #   ch.basic_ack(delivery_tag = method.delivery_tag)
     
channel.basic_consume(callback,
                      queue='graphics',
                      no_ack=True)
for i in [channel.start_consuming,pygame.quit]:

    i()

