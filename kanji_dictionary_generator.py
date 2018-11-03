#simple script to create a dictionary s.t. a character's iso2022_jp code has an enumerated value. This will be used to create one-hot vectors.
import pickle #will be serializing the dictionary so it can be opened later
import os
from os import path
kanji = {}
i = 1
for directory in os.listdir("img"):
	if directory not in kanji:
		kanji.update({ directory:i })
		i += 1
kanji.update({"UNK":i})
binary_file = open('jis_kanji_value_dictionary', 'wb')
pickle.dump(kanji,binary_file)
binary_file.close()
