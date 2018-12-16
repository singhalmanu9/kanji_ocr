import sys
import pickle
import keras
from keras.models import Sequential
from keras.layers import Embedding
from keras.layers import Masking
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Dropout
from keras.layers import Conv2D
from prepare_data import make_train_test;
from keras.layers import MaxPooling2D
from keras.layers import ConvLSTM2D
from keras.layers import UpSampling2D
import numpy as np
import random
import re
import string
from keras import backend as K
import tensorflow as tf
import datetime
x = datetime.datetime.now()
date = str(x)[:-13]
print(K.tensorflow_backend._get_available_gpus())
sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
""" initializing the kanji_enum """
f = open('jis_kanji_value_dictionary', 'rb')
kanji_enum = pickle.loads(f.read())
f.close()
f = open('code_to_hira', 'rb')
code_to_hira = pickle.loads(f.read())
f.close()
list_of_chars = []
for code in code_to_hira:
	if code in kanji_enum:
		list_of_chars.append(code)


f = open('jis_code_indices', 'wb');
pickle.dump(list_of_chars, f);
f.close();
print('Wrote out list_of_chars to jis_code_indices');

input_shape = (63, 64, 1);
#do this for each set of characters? make training and dev set??
#open('path to file', 'r').read(); 
#i THINK i understand what this should be but
train, test = make_train_test(list_of_chars);
trainx = np.array([pair[0] for pair in train]); trainy = np.array([pair[1] for pair in train]);
testx = np.array([pair[0] for pair in test]); testy = np.array([pair[1] for pair in test]);
trainx = trainx.reshape(trainx.shape[0], 63, 64, 1);
testx = testx.reshape(testx.shape[0], 63, 64, 1);

model = Sequential();
model.add(Conv2D(64, kernel_size=(3, 3), activation='tanh', input_shape=input_shape))
model.add(Dropout(.1))
model.add(Conv2D(64, (3, 3), strides = (1,1), activation='tanh'))
model.add(Conv2D(64, (2,2), strides = (1,1), activation='tanh'))
model.add(Dropout(.1))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Conv2D(64, (4, 4), strides = (1,1), activation='tanh'))
model.add(Conv2D(128, (3,3), strides = (1,1), activation='tanh'))
model.add(Conv2D(128, (2,2), strides = (1,1), activation='tanh'))
model.add(Dropout(.1))
model.add(Conv2D(256, (2, 2), activation='tanh'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Conv2D(256, (2, 2), strides = (1,1), activation='tanh'))
model.add(Dropout(.1))
model.add(Conv2D(256, (2, 2), strides = (1,1), activation='tanh'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Flatten())
model.add(Dense(256, activation='tanh'))
model.add(Dense(len(list_of_chars), activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy, optimizer='adam', metrics=['accuracy'])
print(model.summary())


BATCH_SIZE=128
NUM_EPOCHS=128
model.fit(trainx, trainy, epochs = NUM_EPOCHS, batch_size = BATCH_SIZE, validation_data= (testx, testy))
# serialize model to JSON
model_json = model.to_json()
with open(date + "model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")

