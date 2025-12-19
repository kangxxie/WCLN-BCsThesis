from Classes.RabbitMQ_class import RabbitMQ  ;  RMQ = RabbitMQ()
import io
import numpy as np
import tensorflow as tf
import socket, threading, pickle


IP       = 'localhost'
PORT     = 5672 
USERNAME = 'guest'
PASSWORD = 'guest'
EXCHANGE_NAME = 'GUI_counting'


RMQ.createConnection(host=IP, port=PORT, username=USERNAME, password=PASSWORD)
RMQ.declareExchange(EXCHANGE_NAME, exchange_type='direct')

QUEUE_NAME_radar = 'prediction'
ROUTING_KEY_radar = ''
RMQ.declareQueue(name = QUEUE_NAME_radar)
RMQ.bind_exchangeQueue(exchange_name=EXCHANGE_NAME, queue_name=QUEUE_NAME_radar, routing_key=ROUTING_KEY_radar)


# CNN = tf.keras.models.load_model('Trained-models/modello_trained_3.h5')
INTERPRETER = tf.lite.Interpreter(model_path='Trained-models/CNN_model_counting_3targets_2025-08-01_14-34-58-539201-tflite')
INTERPRETER.allocate_tensors()

output_details = INTERPRETER.get_output_details()  # Model has single output.
input_details = INTERPRETER.get_input_details()

RD = np.random.random( size=(50,50))
RA = np.random.random( size=(40,60))
N_TARGETS = []

def callback_radar(ch, method, properties, body):
    global RD, RA, N_TARGETS
    # global CNN, 
    global INTERPRETER, input_details, output_details

    # deserialize
    buffer = io.BytesIO(body)
    npzfile = np.load(buffer)
    temp_RD = npzfile['RD']
    temp_RA = npzfile['RA']
    
    normalized_RD = (temp_RD - temp_RD.min()) / (temp_RD.max() - temp_RD.min())
    normalized_RD = np.expand_dims(normalized_RD, axis=(0,-1))
    
    # predictions = CNN.predict(normalized_RD, verbose=0)

    # N_TARGETS = np.random.randint(0,10)

    X = tf.cast( normalized_RD, tf.float32)
    INTERPRETER.set_tensor(input_details[0]['index'], X)
    INTERPRETER.invoke()
    predictions = INTERPRETER.get_tensor(output_details[0]['index'])
    
    N_TARGETS.append( int(predictions.argmax()) )
    if len(N_TARGETS)>50: N_TARGETS.pop(0)
    # N_TARGETS+=1

    RD= temp_RD
    RA= temp_RA


    print(RD.mean(), RA.mean(), N_TARGETS[-1], len(N_TARGETS))

RMQ.define_consume( queue_name        =QUEUE_NAME_radar,
                    callback_function = callback_radar )




#  SERVER_RD
def func_SERVER_RD():
    global IP
    port = 11111

    SERVER_RD = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER_RD.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    SERVER_RD.bind((IP, port))
    SERVER_RD.listen()

    while True:
        client_socket, client_address = SERVER_RD.accept()
        msg_recv = client_socket.recv(1024)

        data_bytes = pickle.dumps(RD)
        
        client_socket.sendall(len(data_bytes).to_bytes(4, byteorder='big'))
        client_socket.sendall(data_bytes)

        print(msg_recv)

thread = threading.Thread(target=func_SERVER_RD, args=())
thread.start()


#  SERVER_RA
def func_SERVER_RA():
    global IP
    port = 22222

    SERVER_RA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER_RA.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    SERVER_RA.bind((IP, port))
    SERVER_RA.listen()

    while True:
        client_socket, client_address = SERVER_RA.accept()
        msg_recv = client_socket.recv(1024)

        data_bytes = pickle.dumps(RA)
        
        client_socket.sendall(len(data_bytes).to_bytes(4, byteorder='big'))
        client_socket.sendall(data_bytes)

        print(msg_recv)

thread = threading.Thread(target=func_SERVER_RA, args=())
thread.start()


#  SERVER_COUNTING
def func_SERVER_COUNTING():
    global IP
    port = 33333

    SERVER_COUNTING = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER_COUNTING.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    SERVER_COUNTING.bind((IP, port))
    SERVER_COUNTING.listen()

    while True:
        client_socket, client_address = SERVER_COUNTING.accept()
        msg_recv = client_socket.recv(1024)

        data_bytes = pickle.dumps(N_TARGETS)
        client_socket.sendall( data_bytes )

        print(msg_recv)

thread = threading.Thread(target=func_SERVER_COUNTING, args=())
thread.start()


#  SERVER_CHART
def func_SERVER_CHART():
    global IP
    port = 44444

    SERVER_CHART = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER_CHART.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    SERVER_CHART.bind((IP, port))
    SERVER_CHART.listen()

    while True:
        client_socket, client_address = SERVER_CHART.accept()
        msg_recv = client_socket.recv(1024)

        data_bytes = pickle.dumps(N_TARGETS)
        client_socket.sendall( data_bytes )

        print(msg_recv)

thread = threading.Thread(target=func_SERVER_CHART, args=())
thread.start()

RMQ.start_consuming()
