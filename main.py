import socket   #for sockets
import sys  #for exit
import pygame
from objects import *
from thread  import *

players = []
self_id = -1

def parse(data):
    global self_id

    cmd = data[0]
    msg = data[1:]

    if cmd == 'c':
        self_id = int(msg)
    elif cmd == 't':
        params = msg.split(',',1)
        id = int(params[0])
        if id != self_id:
            print "[Player "+str(id+1)+"] "+params[1]

def serverlisten(socket):
    
    while True:
        data = socket.recv(1024)
        if not data:
            break
        cmds = data.split(';')
        for i in cmds:
            if i:
                parse(i)

ip   = raw_input("Server ip: ");
port = input("Server port: ");
try:
    #create an AF_INET, STREAM socket (TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit()

print 'Socket Created'
s.connect((ip,port))
start_new_thread(serverlisten ,(s,))
while 1:
    msg = raw_input()
    msg.replace(';','')
    s.send("t"+msg)

s.close()
