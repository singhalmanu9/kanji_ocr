import sys
import pickle
import keras
from keras.models import Sequential
from keras.layers import LSTM, Embedding
from keras.layers import Masking
from keras.layers import Dense
from keras.layers import TimeDistributed
from keras.layers import Bidirectional
from keras.layers import Flatten
from keras.layers import Dropout
from keras.layers import Conv2D
from prepare_data import make_train_test;

import numpy as np
import random
import re
import string



""" initializing the kanji_enum """
f = open('jis_kanji_value_dictionary', 'rb')
kanji_enum = pickle.loads(f.read())
f.close()

input_shape = (63, 64, 1);
#do this for each set of characters? make training and dev set??
list_of_chars = ['242a', '242b'] #open('path to file', 'r').read(); 
#i THINK i understand what this should be but
train, test = make_train_test(list_of_chars);
trainx = np.array([pair[0] for pair in train]); trainy = np.array([pair[1] for pair in train]);
testx = np.array([pair[0] for pair in test]); testy = np.array([pair[1] for pair in test]);
trainx = trainx.reshape(trainx.shape[0], 63, 64, 1);
trainy = trainy.reshape(trainy.shape[0], 1, len(list_of_chars));

model = Sequential();
model.add(Conv2D(100, kernel_size=(5, 5), activation='relu', input_shape=input_shape))
model.add(Conv2D(100, (4, 4), activation='relu'))
model.add(Conv2D(100, (3, 3), activation='relu'))
model.add(Dropout(.25))
model.add(Flatten())
model.add(Dense(25, activation='relu'))
model.add(Dense(len(list_of_chars), activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.Adadelta(), metrics=['accuracy'])
print(model.summary())


BATCH_SIZE=256
NUM_EPOCHS=2
model.fit(trainx, trainy, epochs = NUM_EPOCHS, batch_size = BATCH_SIZE, validation_data= (testx, testy))
