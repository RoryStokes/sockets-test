import socket
import sys
from objects import *
from thread import *

colours = ['red','blue','green','yellow']
player_count = 0
connections = []
 
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(8)
print 'Socket now listening'
 
def parse(data,player):
    cmd = data[0]
    msg = data[1:]

    if cmd == 't':
        print "[Player "+str(player.id+1)+"] "+msg
        broadcast("t"+str(player.id)+","+msg)
    elif cmd == 'm':
        params = msg.split(',')
        if params >= 2:
            player.x += int(params[0])
            player.y += int(params[1])
        broadcast("m"+str(player.id)+","+params[0]+","+params[1])

def broadcast(data):
    global connections
    data = data+';'
    for i in connections:
        i.sendall(data)

#Function for handling connections. This will be used to create threads
def clientthread(conn):
    global player_count
    global colours
    player = Player()
    player.id = player_count
    player_count += 1
    player.colour = colours[player.id]
    conn.sendall("c"+str(player.id))
    broadcast("a"+str(player.id)+","+str(player.colour)+","+str(player.x)+","+str(player.y))
     
    #infinite loop so that function do not terminate and thread do not end.
    while True:
         
        #Receiving from client
        data = conn.recv(1024)
        if not data:
            break
        cmds = data.split(';')
        for i in cmds:
            parse(i,player)
     
    #came out of loop
    conn.close()
 
#now keep talking with the client
while True:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'New player connected with ' + addr[0] + ':' + str(addr[1])
     
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    connections.append(conn)
    start_new_thread(clientthread ,(conn,))
 
s.close()
