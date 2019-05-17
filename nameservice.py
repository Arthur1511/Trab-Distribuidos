import os
import socket

HOST = socket.gethostbyname(socket.gethostname())

os.system("pyro4-ns -n " + HOST)