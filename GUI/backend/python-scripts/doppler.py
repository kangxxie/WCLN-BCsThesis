# import json
# import numpy as np
# from Classes.FileReader_class import fileReader
# FR = fileReader()
# import numpy as np
# import tensorflow as tf

# def extract_range_doppler(frame_index=0):
#     """
#     Estrae un singolo frame Range-Doppler dal dataset.
#     Args:
#         target_type: 0 per frame senza target, 1 per frame con target
#         frame_index: indice del frame da restituire
#     """
#     filepath = '/Users/alessandro/Desktop/Counting/Dataset/'
#     name='2_targets-2000_28Jul2025_14_35_11'
#     data = FR.load_data(name, filepath)
#     selected_frames = np.array(data['beforeClutterMitig']['RD_list'])
#     # Gestione robusta: accetta sia np.ndarray che lista di frame
#     return {
#         "Range-Doppler Map": selected_frames[10].tolist(),
#         "total_frames": 1,
#         "frame_index": frame_index,
#         "available_frames": selected_frames.shape[0]
#     }

# if __name__ == "__main__":
#     import sys
#     try:
#         frame_index = int(sys.argv[2]) if len(sys.argv) > 2 else 0
#         result = extract_range_doppler(frame_index=frame_index)
#         print(json.dumps(result))
#     except Exception as e:
#         print(json.dumps({"error": str(e)}))

import socket, io, pickle, json
import numpy as np


IP   = 'localhost'
port = 11111
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
RD = pickle.loads(data)
# print(RD.shape)

result = {  "Range-Doppler Map": RD.tolist(),
            "total_frames": 1,
            "frame_index": 0,
            "available_frames": 100 }

print( json.dumps(result) )