from Utilities.BLOCCO_E          import Parameters_Blocco_E  as Parameters
from Utilities.BLOCCO_E.Radar_Blocco_E          import createRadar
from pyav.RabbitMQ_class import RabbitMQ ; RMQ = RabbitMQ()
import numpy as np
import io
from pyav.Time_class import Time; T=Time()
# %-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%
# savingDescription = '5_targets'
# savingpath = 'DataCollected/'
# N_MEAS_TO_COLLECT = 2000
# %-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%


#   i n p u t   c h e c k       ---------------------------------------------------------------------------------------------------------
# if len(sys.argv) not in {1, 3}: 
#     raise ValueError('Launch as:\n\tpython 2_tracking_fromSavedData.py \n\t\tor\n\t2_tracking_fromSavedData.py "emptyrooms/filename_RD" "emptyrooms/filename_RDA"')



IP       = 'localhost'
PORT     = 5672 
USERNAME = 'guest'
PASSWORD = 'guest'
EXCHANGE_NAME = 'GUI_counting'

RMQ.createConnection(host=IP, port=PORT, username=USERNAME, password=PASSWORD)
RMQ.declareExchange(    name=EXCHANGE_NAME, exchange_type='direct')


#   R A D A R       ---------------------------------------------------------------------------------------------------------
radar = createRadar(Parameters.RMin,
                    Parameters.RMax,
                    Parameters.VMin,
                    Parameters.VMax,
                    Parameters.nPointsFFTrange,
                    Parameters.nPointsFFTvel,
                    Parameters.nPointsFFTang,
                    Parameters.T, 
                    Parameters.Nchirp   )



while True:

    radarData = radar.get_radar_data()    
    RDA_orig, RD_orig = radar.createMAP_RDA_RD(radarData)
    
    RA_orig = RDA_orig.mean(axis=1)

    # Serialize it to bytes
    buffer = io.BytesIO()
    np.savez(buffer, RD=RD_orig, RA=RA_orig)
    buffer.seek(0)
    body = buffer.read()

    RMQ.publish(exchange_name=EXCHANGE_NAME, body = body)

    print('published ', T.convert_datetime2str(T.timestamp()))


