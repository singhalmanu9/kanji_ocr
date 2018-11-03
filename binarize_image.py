from scipy.misc import imread, imsave
from collections import Counter
import struct
from PIL import Image, ImageEnhance
import os
files =[]
print("starting file sorting")
for file in os.listdir("img"):
	if "ETL1" in file:
		files.append(file)
print("starting file binarizing")
for fn in files:
	img = imread("img/" + fn,mode = "L")
	binarizes = 1.0* (img > 110)
	imsave("img/" + fn, binarizes)
print("task finished")

