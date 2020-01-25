import os, sys
import socket
from base64 import *
import time


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


while True:
    data = server.recv(socksize)
    cmd = input(data)
    server.sendall(str(cmd).encode())

server.close()

