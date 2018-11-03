import sys
import pickle
from keras.models import Sequential
from keras.layers import LSTM, Embedding
from keras.layers import Masking
from keras.layers import Dense
from keras.layers import TimeDistributed
from keras.layers import Bidirectional
from keras.layers import Flatten
from keras.layers import Dropout
from prepare_data import make_train_test;

import numpy as np
import random
import re
import string



""" initializing the kanji_enum """
f = open('jis_kanji_value_dictionary', 'rb')
kanji_enum = pickle.loads(f.read())
f.close()

input_shape = (64, 63, 1);
#do this for each set of characters? make training and dev set??
list_of_chars = open('path to file', 'r').read(); 
#i THINK i understand what this should be but
train, test = make_train_test(list_of_chars);

model = Sequential();
model.add(Conv2D(100, kernel_size=(5, 5), activation='relu', input_shape=input_shape))
model.add(Conv2D(100, (4, 4), activation='relu'))
model.add(Conv2D(100, (3, 3), activation='relu'))
model.add(Dropout(.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(len(list_of_chars, activation='softmax')))

model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.Adadelta(), metrics=['accuracy'])
print(model.summary())


BATCH_SIZE=256
NUM_EPOCHS=2
model.fit([pair[0] for pair in train], [pair[1] for pair in train],epochs = NUM_EPOCHS, batch_size = BATCH_SIZE, validation_data= ([pair[0] for pair in test], [pair[1] for pair in test]))
