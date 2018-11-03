import os;
from scipy import imread;
import numpy as np;

def make_train_test(list_of_chars):
	allimages = os.listdir('img');

	train_image_target_pairs = {};
	test_image_target_pairs = {};

	for char in list_of_chars:
		char_images = [];
		for filename in allimages:
			if char in filename:
				char_images.append('img/' + imread(filename));
		np.random.shuffle(char_images);
		target = np.zeros(len(list_of_chars));
		target[list_of_chars.indexof(char)] = 1;
		char_targets = [target[:] for i in range(len(char_images))];
		image_target_pairs = zip(char_images, char_targets);

		train_amt = int(.8*len(image_target_pairs));
		train_image_target_pairs.append(image_target_pairs[:train_amt]);
		test_image_target_pairs.append(image_target_pairs[train_amt:])
		
	return train_image_target_pairs, test_image_target_pairs;
