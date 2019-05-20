import json
import codecs
import io
file = codecs.open("Hiragana JIS codes", "r",encoding = "utf8")
lines = file.readlines()
code_to_hira = {}
for line in lines:
	line = line.split(" ")
	code_to_hira[line[2]] = line[9].rstrip()

with io.open("code_to_hira.json","w", encoding='utf8') as json_file:
    json.dump(code_to_hira, json_file, ensure_ascii=False)
file.close()

