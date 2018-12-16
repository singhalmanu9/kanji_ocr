import keras
from keras.models import model_from_json
import os
import pickle
import numpy as np
from scipy.misc import imread

def load_test_images():
	files = os.listdir('test_data/hira_test')
	# print(files[:-10])
	imgs = [imread('test_data/hira_test/' + _, mode = "L") for _ in files]
	return np.array(imgs)

file = open('2018-11-11 20model.json', 'r')
json_model = file.read()
file.close()
model = model_from_json(json_model)
model.load_weights('model.h5')

img = load_test_images()
img = img.reshape(img.shape[0], 63, 64, 1)
print('Loaded test images')
classes = model.predict(img)
#getting top two predictions
indices = np.array([np.argsort(prediction)[:2] for prediction in classes])
indices = np.ndarray.flatten(indices)
with open("jis_code_indices", 'rb') as f:
	x = pickle.loads(f.read())
codes = [x[index] for index in indices]
codeset = set(codes)
print(codeset, "length" ,len(codeset))
