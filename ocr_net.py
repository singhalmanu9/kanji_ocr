import sys
import pickle
import keras
from keras import regularizers
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
from keras.layers import Activation
import numpy as np
import random
import re
import string
from keras import backend as K
import tensorflow as tf
import datetime
import json
import os
from scipy.misc import imread
from keras.optimizers import SGD

x = datetime.datetime.now()
date = str(x)[:-13]
print(K.tensorflow_backend._get_available_gpus())
sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
""" initializing the kanji_enum """

def get_train_test(list_of_chars):
	train_image_target_pairs = [];
	test_image_target_pairs = [];
	"""
	This only trains on characters within the list i.e. no OOV tag.
	"""
	for char in os.listdir('img/'):
		if char == './DS_Store':
			continue
		char_images = []
		for filename in os.listdir('img/' + char):
			char_images.append(imread('img/' + char + '/' + filename))

		target = np.zeros(len(list_of_chars))
		if char in list_of_chars:
			target[list_of_chars.index(char)] = 1 #in vocab
			char_targets = [target for i in range(len(char_images))] 
			image_target_pairs = list(zip(char_images,char_targets))

			train_amt = int(.8*len(image_target_pairs));
			for pair in image_target_pairs[:train_amt]:
				train_image_target_pairs.append(pair)
			for pair in image_target_pairs[train_amt:]:
				test_image_target_pairs.append(pair)
	random.shuffle(train_image_target_pairs)
	random.shuffle(test_image_target_pairs)
	print(len(train_image_target_pairs))
	return train_image_target_pairs, test_image_target_pairs;


with open('cleaned_radical_jis_utf16_dict','r') as f:
	rad_jis_utf16_dict = json.load(f)

for model_key in list(rad_jis_utf16_dict.keys()):
	input_shape = (63, 64, 1)
	list_of_chars = list(rad_jis_utf16_dict[model_key])
	train, test = get_train_test(list_of_chars)
	train = list(zip(*train))
	trainx = np.array(train[0])
	trainy = np.array(train[1])
	test = list(zip(*test))
	testx = np.array(test[0])
	testy = np.array(test[1])
	trainx = trainx.reshape(trainx.shape[0], 63, 64, 1)
	testx = testx.reshape(testx.shape[0], 63, 64, 1)
	class_weights = [0 for _ in range(len(list_of_chars))]
	for y in trainy:
		class_weights[np.argmax(y)] += 1
	model = Sequential()
	model.add(Conv2D(64, 3, 3, border_mode='same', input_shape=input_shape, activation = 'relu',kernel_regularizer=regularizers.l2(0.001)))
	model.add(Conv2D(64, 2, 2, border_mode='same', input_shape=input_shape, activation = 'relu'))
	model.add(Conv2D(64, 1, 1, border_mode='same', input_shape=input_shape, activation = 'relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Conv2D(128, 3, 3, border_mode='same', input_shape=input_shape, activation = 'relu',kernel_regularizer=regularizers.l2(0.001)))
	model.add(Conv2D(128, 2, 2, border_mode='same', input_shape=input_shape, activation = 'relu'))
	model.add(Conv2D(128, 1, 1, border_mode='same', input_shape=input_shape, activation = 'relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.25))
	model.add(Conv2D(256, 3, 3, border_mode='same',activation = 'relu',kernel_regularizer=regularizers.l2(0.001)))
	model.add(Conv2D(256, 2, 2, border_mode='same',activation = 'relu'))
	model.add(Conv2D(256, 1, 1, border_mode='same',activation = 'relu'))
	model.add(Conv2D(256, 3, 3,activation = 'relu',kernel_regularizer=regularizers.l2(0.001)))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.25))
	model.add(Conv2D(512, 3, 3, border_mode='same',activation = 'relu',kernel_regularizer=regularizers.l2(0.001)))
	model.add(Conv2D(512, 2, 2, border_mode='same',activation = 'relu'))
	model.add(Conv2D(512, 1, 1, border_mode='same',activation = 'relu'))  
	model.add(Conv2D(512, 3, 3,activation = 'relu',kernel_regularizer=regularizers.l2(0.001)))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.25))
	model.add(Flatten())
	model.add(Dense(4096,activation = 'relu',kernel_regularizer=regularizers.l2(0.001)))
	model.add(Dropout(0.5))

	model.add(Dense(len(list_of_chars), activation='softmax'))

	opt = SGD(lr=0.005,decay = 1e-5)
	model.compile(loss='categorical_crossentropy', 
	optimizer=opt, metrics=['accuracy','categorical_crossentropy'])
	print(model.summary())
	print(class_weights)
	print(len(list_of_chars))
	print(list_of_chars)
	print(model_key)
	

	BATCH_SIZE= 256
	NUM_EPOCHS=256
	model.fit(trainx, trainy, epochs = NUM_EPOCHS, batch_size = BATCH_SIZE, validation_data= (testx, testy), class_weight = class_weights)
	# serialize model to JSON
	model_json = model.to_json()
	with open(model_key + "model.json", "w") as json_file:
		json_file.write(model_json)
	# serialize weights to HDF5
	model.save_weights("model.h5")
	print("Saved model to disk")
	break

