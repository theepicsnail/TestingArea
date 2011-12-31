import socket

UDP_IP="66.96.251.117"
UDP_PORT=5005

sock = socket.socket( socket.AF_INET, # Internet
                      socket.SOCK_DGRAM ) # UDP

i = 0
import time
while True:
    i=i+1
    time.sleep(.5)
    sock.sendto(str(time.time()),(UDP_IP,UDP_PORT))

