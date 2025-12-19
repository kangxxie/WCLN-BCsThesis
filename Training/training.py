import dill, os
import numpy as np
import matplotlib.pyplot as plt
from Classes.cnn_model import Count
from tqdm import tqdm
from pyav.Dataset_class import Dataset 
from pyav.Statistic_class import Statistic ; S = Statistic()
from pyav.Time_class      import Time      ; T = Time()


# parameters
DATA_PATH = '../Dataset/'
FILENAMES = ['0_targets-2000_28Jul2025_14_27_14',  '1_targets-2000_28Jul2025_14_31_03']#, '2_targets-2000_28Jul2025_14_35_11']#, '3_targets-2000_28Jul2025_14_46_06', '4_targets-2000_28Jul2025_14_51_16', '5_targets-2000_28Jul2025_15_00_32']

SAVING_MODEL_PATH = 'Saved-models/'

training_size = 0.5

EPOCHS = 15
BATCH_SIZE = 128





X = []
Y = []
for name in FILENAMES:
    f = open(os.path.join(DATA_PATH, name), 'rb')
    data = dill.load(f)
    RD_list = data['beforeClutterMitig']['RD_list']
    X += RD_list
    Y += [int(name[0])] * len(RD_list)

X = np.array(X)
Y = np.array(Y)

indices = np.arange(len(X))
np.random.shuffle(indices)
X = X[indices]
Y = Y[indices]

split = int(training_size * len(X))
X_TRAINING = X[:split]
Y_TRAINING = Y[:split]
X_VALIDATION = X[split:]
Y_VALIDATION = Y[split:]


X_TRAINING   = np.expand_dims(X_TRAINING, axis=-1)
X_VALIDATION = np.expand_dims(X_VALIDATION, axis=-1)

DS = Dataset (  X = X_TRAINING, 
                Y = Y_TRAINING,
                validation = (X_VALIDATION, Y_VALIDATION) )


DS.map_function( S.normalize, a=0, b=1 )




input_shape  = DS.get_inputShape()
output_shape = DS.get_outputShape_forClassification()

cnn_counter = Count( output_shape=output_shape, input_shape=input_shape)
cnn_counter.printSummary()


for e in range(EPOCHS):
    batches = DS.get_batches( batch_size=BATCH_SIZE )
    
    print( 'EPOCH '+str(e))
    for i in tqdm(range(len(batches))):

        x, y = batches[i]
        loss_value = cnn_counter.train_step(x, y)

        cnn_counter.updateHistory(  x=DS.X, 
                                    y=DS.Y,
                                    x_valid=DS.X_valid,
                                    y_valid=DS.Y_valid  )

    cnn_counter.print_trainingStatus(   x=DS.X, 
                                        y=DS.Y,
                                        x_valid=DS.X_valid,
                                        y_valid=DS.Y_valid  )
    

    
cnn_counter.show()



if input('\nSave? [y/n]: ' ) == 'y':
    T.convert_datetime2str(T.timestamp())
    filename = 'CNN_model_counting_' +      \
                str(len(np.unique(Y_TRAINING)))+'targets_'+         \
                T.convert_datetime2str(T.timestamp()).replace(' ','_').replace('.','-').replace(':','-')
    #! add accuracy in filename
    
    # cnn_counter.save(os.path.join(SAVING_MODEL_PATH, filename ))
    cnn_counter.tflite_save( os.path.join(SAVING_MODEL_PATH, filename) )