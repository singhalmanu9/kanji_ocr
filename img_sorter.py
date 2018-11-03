import os
from os import path
from collections import Counter
charcodes = Counter()
for file in os.listdir("img"):
	if not path.isdir("img/" + file):
		x = file.split("_")
		charcodes[x[2]] += 1
for charcode in charcodes:
	print("making directory: img/" + charcode)
	try:
		os.mkdir("img/" + charcode)
	except:
		print("directory already exists!")
	print("success! directory img/"+ charcode + " created.")
print("now moving files into their appropriate folders.")
for file in os.listdir("img"):
	if not path.isdir("img/"+file):
		x = file.split("_")
		os.rename("img/" + file, "img/" + x[2] + "/" + file)
	else:
		print("chief...")