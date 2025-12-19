
import tensorflow as tf
from pyav.DeepLearning_class import DeepLearning ; DL = DeepLearning()


#!   M O D E L   ----------------------------------------------------------------------------------------------------------------------------------
name = 'Saved-models/CNN_model_counting_3targets_2025-08-01_14-34-58-539201'
loaded_model = DL.load_model(name +'.h5')
#!  -----------------------------------------------------------------------------------------------------------------------------------------------



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
# with open(name+'.tflite', 'wb') as f:
with open(name+'-tflite', 'wb') as f:
    f.write(tflite_model)