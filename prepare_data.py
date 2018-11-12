import os;
from scipy.misc import imread;
import numpy as np;

def make_train_test(list_of_chars):

	train_image_target_pairs = [];
	test_image_target_pairs = [];

	for char in list_of_chars:
		#print('Searching in: ' + 'img/' + char);
		allimages = os.listdir('img/' + char);
		#print('Found ' + str(len(allimages)) + ' images')
		char_images = [];
		for filename in allimages:
			char_images.append(imread('img/' + char + '/' + filename));
		np.random.shuffle(char_images);
		target = np.zeros(len(list_of_chars));
		target[list_of_chars.index(char)] = 1;
		#print('Target should look like: ', str(target));
		char_targets = [target[:] for i in range(len(char_images))];
		image_target_pairs = list(zip(char_images, char_targets));
		#print('Created ' + str(len(image_target_pairs)) + ' image target pairs')

		train_amt = int(.8*len(image_target_pairs));
		[train_image_target_pairs.append(pair) for pair in image_target_pairs[:train_amt]];
		[test_image_target_pairs.append(pair) for pair in image_target_pairs[train_amt:]]

	np.random.shuffle(train_image_target_pairs); np.random.shuffle(test_image_target_pairs);
	return train_image_target_pairs, test_image_target_pairs;

