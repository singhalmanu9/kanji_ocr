import sys

from keras.models import Sequential
from keras.layers import LSTM, Embedding
from keras.layers import Masking
from keras.layers import Dense
from keras.layers import TimeDistributed
from keras.layers import Bidirectional
from keras.layers import Flatten

import numpy as np
import random
import re
import string
