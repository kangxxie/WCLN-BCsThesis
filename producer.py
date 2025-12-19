
from pyav.RabbitMQ_class import RabbitMQ ; RMQ = RabbitMQ()
import dill, io, time
import numpy as np

IP       = 'localhost'
PORT     = 5672 
USERNAME = 'guest'
PASSWORD = 'guest'
EXCHANGE_NAME = 'GUI_counting'

RMQ.createConnection(host=IP, port=PORT, username=USERNAME, password=PASSWORD)
RMQ.declareExchange(    name=EXCHANGE_NAME, exchange_type='direct')



PATH = 'Dataset/'
FILENAME = '2_targets-2000_28Jul2025_14_35_11'

f = open (PATH+FILENAME, 'rb')
obj = dill.load(f)

RD_list  = obj['beforeClutterMitig']['RD_list']
RDA_list = obj['beforeClutterMitig']['RDA_list']
RA_list  = [ RDA.mean(axis=1) for RDA in RDA_list]

for i in range(1000):
    index = np.random.randint(0,len(RD_list))
    RD = RD_list[index]
    RA = RA_list[index] 

    # Serialize it to bytes
    buffer = io.BytesIO()
    np.savez(buffer, RD=RD, RA=RA)
    buffer.seek(0)
    body = buffer.read()

    RMQ.publish(exchange_name=EXCHANGE_NAME, body = body)

    print(RD.mean(), RA.mean())
    time.sleep(0.5)