import socket, io, pickle
import numpy as np


IP   = 'localhost'
port = 22222
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, port))
    
client.send('ready'.encode('utf-8'))

# First receive 4 bytes for length
length_bytes = client.recv(4)
data_length = int.from_bytes(length_bytes, byteorder='big')

# Receive the actual data
data = b''
while len(data) < data_length:
    packet = client.recv(data_length - len(data))
    if not packet:
        break
    data += packet

# Deserialize
RA = pickle.loads(data)
print(RA.shape)
