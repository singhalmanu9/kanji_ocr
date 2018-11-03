import pickle
code_to_hira = {}
hira_to_code = {}

with open("Hiragana JIS codes") as f:
	x = f.readlines()
for line in x:
	code = line.split(' ')[2]
	hira = line.split(' ')[7]
	code_to_hira.update({code:hira})
	hira_to_code.update({hira:code})
f = open('code_to_hira','wb')
pickle.dump(code_to_hira,f)
f.close()
f = open('hira_to_code','wb')
pickle.dump(hira_to_code,f)
f.close()
