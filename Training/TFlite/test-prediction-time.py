import numpy as np
from pyav.DeepLearning_class import DeepLearning ; DL = DeepLearning()
import tensorflow as tf
import time

#!   M O D E L   ----------------------------------------------------------------------------------------------------------------------------------
loaded_model = DL.load_model( filename='Saved-models/CNN_model_counting_3targets_2025-08-01_14-34-58-539201.h5')
#!  -----------------------------------------------------------------------------------------------------------------------------------------------


'''
#!   S A V E   T F   M O D E L   ----------------------------------------------------------------------------------------------------------------------------------
converter = tf.lite.TFLiteConverter.from_keras_model(loaded_model)
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
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)



'''

#!   L O A D   T F   M O D E L   ----------------------------------------------------------------------------------------------------------------------------------

batch_shape = (1,49,55,1)

interpreter = tf.lite.Interpreter(model_path='Saved-models/CNN_model_counting_3targets_2025-08-01_14-34-58-539201-tflite')
interpreter.allocate_tensors()

output_details = interpreter.get_output_details()  # Model has single output.
input_details = interpreter.get_input_details()

# Example: single input



#resize
interpreter.resize_tensor_input(input_details[0]['index'], batch_shape)
interpreter.allocate_tensors()



for i in range(100):

    X = tf.cast( np.random.random( size=(batch_shape)), tf.float32)


    start_time = time.time()
    
    # input_data = tf.constant(1., shape=[1, 5,49,1])
    interpreter.set_tensor(input_details[0]['index'], X)

    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])
    end_time = time.time()


    inference_time = (end_time - start_time) *1000   # milliseconds
    print(f"tf lite: {inference_time:.3f} ms")


    start_time = time.time()
    
    loaded_model.predict(X, verbose=0)
    end_time = time.time()


    inference_time = (end_time - start_time) *1000   # milliseconds
    print(f"model: {inference_time:.3f} ms\n\n")

    #!----

    

    


# input_data = np.array([my_input_data], dtype=np.float32)
# interpreter.set_tensor(input_details[0]['index'], X[:1])
# interpreter.invoke()
# output_data = interpreter.get_tensor(output_details[0]['index'])
