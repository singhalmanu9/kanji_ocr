import os
from collections import Counter
charcodes = Counter()
for file in os.listdir("img"):
	if "242b" in file:
		charcodes[file] += 1
for charcode in charcodes:
	print(charcode, charcodes[charcode])
