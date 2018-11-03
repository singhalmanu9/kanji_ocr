import sys

from keras.models import Sequential
from keras.layers import LSTM, Embedding
from keras.layers import Masking
from keras.layers import Dense
from keras.layers import TimeDistributed
from keras.layers import Bidirectional
from keras.layers import Flatten
from keras.layers import Dropout

import numpy as np
import random
import re
import string


input_shape = (64, 63, 1);

list_of_chars = open('path to file', 'r').read();

train, test = prepare_data(list_of_chars);

model = Sequential();
model.add(Conv2D(100, kernel_size=(5, 5), activation='relu', input_shape=input_shape))
model.add(Conv2D(100, (4, 4), activation='relu'))
model.add(Conv2D(100, (3, 3), activation='relu'))
model.add(Dropout(.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(.5))
model.add(Dense(len(list_of_chars, activation='softmax')))

model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.Adadelta(), metrics=['accuracy'])

model.fit([pair[0] for pair in train], [pair[1] for pair in train], validation_data= ([pair[0] for pair in test], [pair[1] for pair in test]))