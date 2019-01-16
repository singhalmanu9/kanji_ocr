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
import json
import os
from scipy.misc import imread

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
		np.random.shuffle(char_images)
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

	"""
	This trains on every single character for each net.
	"""
	# i = 0
	# for char in os.listdir('img/'):
	# 	if char == './DS_Store':
	# 		continue
	# 	char_images = []
	# 	for filename in os.listdir('img/' + char):
	# 		char_images.append(imread('img/' + char + '/' + filename))
	# 	np.random.shuffle(char_images)
	# 	target = np.zeros(len(list_of_chars) + 1)
	# 	if char in list_of_chars:
	# 		target[list_of_chars.index(char)] = 1 #in vocab
	# 	else:
	# 		target[-1] = 1 #OOV
	# 	char_targets = [target for i in range(len(char_images))] 
	# 	image_target_pairs = list(zip(char_images,char_targets))
	# 	train_amt = int(.8*len(image_target_pairs));
	# 	[train_image_target_pairs.append(pair) for pair in image_target_pairs[:train_amt]];
	# 	[test_image_target_pairs.append(pair) for pair in image_target_pairs[train_amt:]]


	# for char in list_of_chars:
	# 	#print('Searching in: ' + 'img/' + char);
	# 	allimages = os.listdir('img/' + char);
	# 	#print('Found ' + str(len(allimages)) + ' images')
	# 	char_images = [];
	# 	for filename in allimages:
	# 		char_images.append(imread('img/' + char + '/' + filename));
	# 	np.random.shuffle(char_images);
	# 	target = np.zeros(len(list_of_chars));
	# 	target[list_of_chars.index(char)] = 1;
	# 	#print('Target should look like: ', str(target));
	# 	char_targets = [target[:] for i in range(len(char_images))];
	# 	image_target_pairs = list(zip(char_images, char_targets));
	# 	#print('Created ' + str(len(image_target_pairs)) + ' image target pairs')

	# 	train_amt = int(.8*len(image_target_pairs));
	# 	[train_image_target_pairs.append(pair) for pair in image_target_pairs[:train_amt]];
	# 	[test_image_target_pairs.append(pair) for pair in image_target_pairs[train_amt:]]

	return train_image_target_pairs, test_image_target_pairs;


with open('radical_jis_utf16_dict','r') as f:
	rad_jis_utf16_dict = json.load(f)

for model_key in list(rad_jis_utf16_dict.keys()):
	input_shape = (63, 64, 1)
	list_of_chars = list(rad_jis_utf16_dict[model_key].keys())
	train, test = get_train_test(list_of_chars)
	trainx = np.array([pair[0] for pair in train])
	trainy = np.array([pair[1] for pair in train])
	testx = np.array([pair[0] for pair in test])
	testy = np.array([pair[1] for pair in test])
	trainx = trainx.reshape(trainx.shape[0], 63, 64, 1)
	testx = testx.reshape(testx.shape[0], 63, 64, 1)

	model = Sequential()
	model.add(Conv2D(64, 3, 3, border_mode='same', input_shape=input_shape, activation = 'relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Conv2D(128, 3, 3, border_mode='same',activation = 'relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.07))
	model.add(Conv2D(256, 3, 3, border_mode='same',activation = 'relu'))
	model.add(Conv2D(256, 3, 3,activation = 'relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.07))
	model.add(Conv2D(512, 3, 3, border_mode='same',activation = 'relu'))
	model.add(Conv2D(512, 3, 3,activation = 'relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.07))
	model.add(Flatten())
	model.add(Dense(4096,activation = 'relu'))
	model.add(Dropout(0.1))
	model.add(Dense(4096,activation = 'relu'))
	model.add(Dropout(0.1))
	model.add(Dense(len(list_of_chars), activation='softmax'))
	# model.add(Conv2D(64, kernel_size=(3, 3), activation='tanh', input_shape=input_shape))
	# model.add(Dropout(.1))
	# model.add(Conv2D(64, (3, 3), strides = (1,1), activation='tanh'))
	# model.add(Conv2D(64, (2,2), strides = (1,1), activation='tanh'))
	# model.add(Dropout(.1))
	# model.add(MaxPooling2D(pool_size=(2,2)))
	# model.add(Conv2D(128, (4, 4), strides = (1,1), activation='tanh'))
	# model.add(Conv2D(128, (3,3), strides = (1,1), activation='tanh'))
	# model.add(Conv2D(128, (2,2), strides = (1,1), activation='tanh'))
	# model.add(Dropout(.1))
	# model.add(Conv2D(128, (2, 2), activation='tanh'))
	# model.add(MaxPooling2D(pool_size=(2,2)))
	# model.add(Conv2D(256, (2, 2), strides = (1,1), activation='tanh'))
	# model.add(Dropout(.1))
	# model.add(Conv2D(256, (2, 2), strides = (1,1), activation='tanh'))
	# model.add(MaxPooling2D(pool_size=(2,2)))
	# model.add(Flatten())
	# model.add(Dense(256, activation='tanh'))
	# model.add(Dense(len(list_of_chars) + 1, activation='softmax'))

	model.compile(loss=keras.losses.categorical_crossentropy, optimizer='adam', metrics=['accuracy'])
	print(model.summary())

	d = {i: 1 for i in range(0, len(list_of_chars))};
	#d[len(list_of_chars)] = .1;

	BATCH_SIZE=256
	NUM_EPOCHS=64
	model.fit(trainx, trainy, epochs = NUM_EPOCHS, batch_size = BATCH_SIZE, validation_data= (testx, testy), class_weight = d);
	# serialize model to JSON
	model_json = model.to_json()
	with open(model_key + "model.json", "w") as json_file:
		json_file.write(model_json)
	# serialize weights to HDF5
	model.save_weights("model.h5")
	print("Saved model to disk")
	break;

