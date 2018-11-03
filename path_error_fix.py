import os
files =[]
print("starting file sorting")
for file in os.listdir("img"):
	if "ETL" in file:
		files.append(file)
for file in files:
	os.remove(file)
print("removed files placed in wrong directory")
