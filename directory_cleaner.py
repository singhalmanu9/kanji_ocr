import os
from os import path
import shutil
for file in os.listdir("img"):
	if file[-4:] == ".png":
		print("removing file:" + file)
		shutil.rmtree("img/" + file)
