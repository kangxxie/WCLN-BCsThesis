# import tensorflow as tf
# import numpy as np

# class CNNModel:
#     def __init__(self, input_shape, num_classes): # costruttore: mappe range doppler con 34 range e 49 doppler, con 1 canale (grayscale) e 2 classi (target e non target).
#         self.model = self.build_model(input_shape, num_classes)

#     def build_model(self, input_shape, num_classes):
#         model = tf.keras.Sequential()
#         model.add(tf.keras.layers.InputLayer(input_shape=input_shape))
#         model.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape)) # è il primo che riceve i dati grezzi e deve sapere la forma dell’input

#         model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
#         model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))

#         model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
#         model.add(tf.keras.layers.Flatten()) # Appiattisce le feature map 2D in un vettore 1D per poterle passare ai layer densi (fully connected)
#         model.add(tf.keras.layers.Dense(32, activation='relu')) # Layer denso (fully connected) con 32 neuroni
#         model.add(tf.keras.layers.Dense(num_classes, activation='softmax'))

#         model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
#         return model

#     def train(self, train_data, train_labels, epochs, batch_size, validation_data):
#         history = self.model.fit(train_data, train_labels, epochs=epochs, batch_size=batch_size, validation_data=validation_data)
#         #oggetto history contiene l’andamento di loss e accuracy durante il training
#         return history

#     def evaluate(self, test_data, test_labels):
#         loss, accuracy = self.model.evaluate(test_data, test_labels)
#         return loss, accuracy

#     def predict(self, data):
#         predictions = self.model.predict(data)
#         return np.argmax(predictions, axis=1)
    
#     # predictions è un array di forma (numero_campioni, numero_classi), dove ogni riga contiene le probabilità (o punteggi) per ciascuna classe. 
#     # Mettendo axis=1, np.argmax restituisce l'indice della classe con la probabilità più alta per ogni campione.




import tensorflow as tf
from pyav.Printing_class import Printing
import numpy as np

'''
    TRAINING
'''


class Count(tf.keras.Model):
    def __init__(self, output_shape, input_shape = None, learning_rate = 1e-2 ):
        super().__init__()

        self.inputShape =  input_shape
        self.outputShape=  output_shape

        self.model       =  self.build_cnn_model( )

        self.optimizer  = tf.keras.optimizers.Adam(learning_rate=learning_rate) 

        self.history = {'t_loss':[] , 't_acc':[], 'v_loss':[] , 'v_acc':[]}


    def build_cnn_model(self, ):
        cnn_model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(filters=64, kernel_size=(3,3), activation=tf.nn.relu, input_shape = self.inputShape ), 
            tf.keras.layers.MaxPool2D(pool_size=(2,2)),
             
            tf.keras.layers.Conv2D(filters=32, kernel_size=(3,3), activation=tf.nn.relu),
            tf.keras.layers.MaxPool2D(pool_size=(2,2)),

            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(16, activation=tf.nn.relu),

            tf.keras.layers.Dense(self.outputShape, activation=tf.nn.softmax)])

        return cnn_model


    def printSummary(self,):
        self.model.summary()


    def evaluate(self, X, Y):
        return sum(np.argmax( self.model(X), axis =1 ) == Y.squeeze())/ len(Y)
    
    def call(self, X):
        prediction = self.model(X)
        return prediction
    
    @tf.function
    def train_step(self, x, y):
        with tf.GradientTape() as tape:
            predictions = self.model(x) # (batch_size,10)
            
            loss = tf.keras.losses.sparse_categorical_crossentropy(y, predictions)

        grads = tape.gradient(loss, self.model.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))

        return loss
    

    def print_trainingStatus(self, x, y, x_valid, y_valid):
        print('Training: loss {:.6f} -  accuracy {:.2f}'.format(   tf.reduce_mean(tf.keras.losses.sparse_categorical_crossentropy(y, self.model(x))).numpy(),
                                                                    self.evaluate(x, y)) , 
                                                                    end='    ---    ')
        
        print('Validation: loss {:.6f} -  accuracy {:.2f}'.format( tf.reduce_mean(tf.keras.losses.sparse_categorical_crossentropy(y_valid, self.model(x_valid) )).numpy(),
                                                                    self.evaluate(x_valid, y_valid)) )
    
    def updateHistory(self, x, y, x_valid, y_valid):
        self.history['t_loss'].append( tf.reduce_mean(tf.keras.losses.sparse_categorical_crossentropy(y, self.model(x))).numpy() )
        self.history['v_loss'].append( tf.reduce_mean(tf.keras.losses.sparse_categorical_crossentropy(y_valid, self.model(x_valid) )).numpy() ) 

        self.history['t_acc'].append( self.evaluate(x, y) ) 
        self.history['v_acc'].append( self.evaluate(x_valid, y_valid) )

    def show(self):
        printer = Printing('')
        printer.create_Plot(    'Loss',
                                curves={    'A' :   {   'data_y'        :   self.history['t_loss'],                                         #   Y
                                                        'pen'           :   (0,255,0,255),
                                                        'symbolBrush'   :   None,
                                                        'symbolPen'     :   None    },

                                            'B' :   {   'data_y'        :   self.history['v_loss'],     #   Y
                                                        'pen'           :   (255,0,0,255)   }
                                                    },  
                                axesLabels=[ ('iter',''), ('loss', ''), None, None ],
                                show_BottomAxis = True )
        
        printer.create_Plot(    'Accuracy',
                                curves={    'A' :   {   'data_y'        :   self.history['t_acc'],                                         #   Y
                                                        'pen'           :   (0,255,0,255),
                                                        'symbolBrush'   :   None,
                                                        'symbolPen'     :   None    },

                                            'B' :   {   'data_y'        :   self.history['v_acc'],     #   Y
                                                        'pen'           :   (255,0,0,255)   }
                                                    },  
                                axesLabels=[ ('iter',''), ('loss', ''), None, None ],
                                show_BottomAxis = True )
        
        printer.show()

    def save(self, filename):
        self.model.save(filename+ '.h5')

    def tflite_save(self, filename):
        
        converter = tf.lite.TFLiteConverter.from_keras_model(self.model)
        # For quantization (optional):
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        # Enable resource variables
        converter.experimental_enable_resource_variables = True

        # Allow Select TF Ops to handle TensorListReserve, etc.
        converter.target_spec.supported_ops = [
            tf.lite.OpsSet.TFLITE_BUILTINS,
            tf.lite.OpsSet.SELECT_TF_OPS
        ]
        converter._experimental_lower_tensor_list_ops = False
        tflite_model = converter.convert()
        # Save to .tflite file
        # with open(name+'.tflite', 'wb') as f:
        with open(filename+'-tflite', 'wb') as f:
            f.write(tflite_model)




