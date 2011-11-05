#!/usr/bin/env python

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='graphics')
def send(msg):
    print "P out",msg,type(msg)
    channel.basic_publish(exchange='',
                      routing_key='graphics',
                      body=msg)
def setColor(r=0,g=0,b=0):
    send("Color({},{},{})".format(r,g,b))
def drawLine(x,y,x2,y2):
    send("Line({},{},{},{})".format(x,y,x2,y2))
def clear():
    send("Clear()")
def flip():
    send("Flip()")



econnection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
echannel = econnection.channel()
echannel.exchange_declare(exchange="events",type="fanout")
result = echannel.queue_declare(exclusive=True)
queue_name = result.method.queue

echannel.queue_bind(exchange='events',
                    queue=queue_name)


lx=0
ly=0
def callback(ch, method, properties, body):
    global lx,ly
    d = eval(body)
    print "P in",body
    if d["type"]==4:
        setColor(255,255,255)
        clear()

        setColor(0,0,0)
        drawLine(lx,ly,d["pos"][0],d["pos"][1])
        flip()
    if d["type"]==5:
        lx,ly=d["pos"]
echannel.basic_consume(callback,
                       queue=queue_name,
                       no_ack=True)

echannel.start_consuming()


