import keras
from keras.models import model_from_json
import os
import pickle
import numpy as np
from scipy.misc import imread;

def load_test_images():
	files = os.listdir('img/hira_test');
	# print(files[:-10])
	imgs = [imread('img/hira_test/' + _, mode = "L") for _ in files];
	return np.array(imgs);

file = open('model.json', 'r');
json_model = file.read();
file.close();
model = model_from_json(json_model);
model.load_weights('model.h5');

img = load_test_images();
img = img.reshape(img.shape[0], 63, 64, 1);
print('Loaded test images');
classes = model.predict(img);
indices = [np.argmax(prediction) for prediction in classes];

with open("jis_code_indices", 'rb') as f:
	x = pickle.loads(f.read());
codes = [x[index] for index in indices];
print(set(codes));
