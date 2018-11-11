from scipy.misc import imread, imsave
from collections import Counter
import struct
from PIL import Image, ImageEnhance
import os

files = os.listdir("img/test");
print("starting file binarizing")
for fn in files:
	img = imread("img/test/" + fn, mode = "L")
	binarizes = 1.0 * (img < 110)
	imsave("img/test/" + fn, binarizes)
print("task finished")

