# import json
# import numpy as np
# from Classes.FileReader_class import fileReader
# import tensorflow as tf
 
# FR = fileReader()
 
# def predict_targets(frame_index=0):
#     # Usa il modello CNN per predire il numero di target in un frame Range-Doppler.
#     # Il frame_index è lo stesso passato a doppler.py, così la prediction è sincronizzata con la visualizzazione.
   
#     # Carica il modello
#     model = tf.keras.models.load_model('/Users/alessandro/Desktop/Counting/Trained-models/modello_trained.h5')
#     # Carica i dati
#     filepath = '/Users/alessandro/Desktop/Counting/Dataset/'
#     name = '2_targets-2000_28Jul2025_14_35_11'
#     data = FR.load_data(name, filepath)
#     selected_frames = np.array(data['beforeClutterMitig']['RD_list'])
#     frame = selected_frames[frame_index]
#     frame = np.expand_dims(frame, axis=0)  
#     frame = np.expand_dims(frame, axis=-1)  
#     # Preprocessing: aggiungi batch dimension e normalizza se necessario
#     prediction = model.predict(frame, verbose=0)
#     num_targets = np.argmax(prediction)
#     return {
#         "frame_index": frame_index,
#         "predicted_targets": num_targets.tolist()
#     }
 
# if __name__ == "__main__":
#     import sys
#     try:
#         frame_index = int(sys.argv[1]) if len(sys.argv) > 1 else 0
#         result = predict_targets(frame_index=frame_index)
#         print(json.dumps(result))
#     except Exception as e:
#         print(json.dumps({"error": str(e)}))
 

import socket, io, pickle, json
import numpy as np


IP   = 'localhost'
port = 33333
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, port))
    
client.send('ready'.encode('utf-8'))


body = client.recv(1024)
N_TARGETS = pickle.loads(body)

# print(N_TARGETS)


result = {
        "frame_index": 0,
        "predicted_targets": N_TARGETS[-1:]
    }


print(json.dumps(result))
