import time
import curses
import os, sys
import socket
from base64 import *

ENTER_KEY = (curses.KEY_ENTER, ord('\n'), ord('\r'))

try:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
except IndexError:
    print("You must specify a host IP address and port number!")
    print("usage: ./handler_client.py 192.168.1.4 4444")
    sys.exit()

socksize = 4096
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.connect((HOST, PORT))
    print("[+] Connection established!")
    print("[+] Type ':help' to view commands.")
except:
    print("[!] Connection error!")
    sys.exit(2)

def run(win, timeout=5):
    curses.echo()
    win.timeout(0) # Non-block read.

    line = 0

    while True:
        data = server.recv(socksize)
    
        s = []
        cmd = ""
        start = time.time()
        run = True
        while run:
            c = win.getch()
            time_taken = time.time() - start

            if c < 0:
                pass
            elif c in ENTER_KEY:
                break
            else:
                s.append(chr(c))
                cmd += chr(c)
                run = False

            if time_taken >= timeout:
                # Out of time.
                s.append(-1)
                run = False

        server.sendall(str(cmd).encode())

curses.wrapper(run)
server.close()
