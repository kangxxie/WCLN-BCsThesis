import socket, io, pickle
import numpy as np


IP   = 'localhost'
port = 33333
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, port))
    
client.send('ready'.encode('utf-8'))


body = client.recv(1024)
N_TARGETS = pickle.loads(body)

print(N_TARGETS)


