
import socket, io, pickle, json
import numpy as np


IP   = 'localhost'
port = 44444
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, port))
    
client.send('ready'.encode('utf-8'))


body = client.recv(1024)
N_TARGETS = pickle.loads(body)

# print(N_TARGETS)


result ={
        "hours": [f"{i:02d}" for i in np.arange(len(N_TARGETS))],
        "targets": N_TARGETS,
        "total_detections": len(N_TARGETS),
        "peak_hour": max(N_TARGETS),
        "avg_per_hour": round(np.mean(N_TARGETS),2)
    }


print(json.dumps(result))



