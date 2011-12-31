import socket

UDP_IP=""
UDP_PORT=5005

sock = socket.socket( socket.AF_INET, # Internet
                      socket.SOCK_DGRAM ) # UDP
sock.bind( (UDP_IP,UDP_PORT) )


last = None

missed = 0
swapped = 0
repeats = 0
seen = set()
total = 1
import time
while True:
    data, addr = sock.recvfrom( 1024 ) # buffer size is 1024 bytes
    cur = float(data)
    print (time.time()-cur)*500
