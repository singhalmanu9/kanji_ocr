import json
import os
with open('radical_jis_utf16_dict','r') as f:
	rad_jis_utf16_dict = json.load(f)
new_dict = {}
for model_key in list(rad_jis_utf16_dict.keys()):
	x = []
	for character_code in rad_jis_utf16_dict[model_key]:
		if character_code in os.listdir('img/'):
			x.append(character_code)
		else:
			print(character_code, "not present in img/")
	if len(x):
		new_dict[model_key] = x
print(len(new_dict))
print(len(rad_jis_utf16_dict))

with open('cleaned_radical_jis_utf16_dict', 'w') as outfile:  
    json.dump(new_dict, outfile)