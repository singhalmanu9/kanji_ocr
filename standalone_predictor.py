from tkinter import *
from PIL import Image, ImageDraw, ImageOps
master = Tk()
width=64 * 8
height=63 * 8
image_name = "image query.png"

def gui_setup():

	image_name = "image query.png"
	w = Canvas(master, width=width, height=height, borderwidth = 4)
	image = Image.new("L",(width, height), "white")
	draw = ImageDraw.Draw(image)
	def predict():
		import keras
		from keras.models import model_from_json
		import os
		import numpy as np
		from scipy.misc import imread
		import json
		import codecs
		
		# save image and stop all further user actions on canvas
		image.save(image_name)
		w.unbind("<B1-Motion>")
		w.unbind("<B3-Motion>")
		b.config(state="disabled")
		w.delete("all")
		predicted_kanji.delete(1.0,END)
		#load model
		file = open('hiraganamodel.json', 'r')
		json_model = file.read()
		file.close()
		model = model_from_json(json_model)
		model.load_weights('model.h5')

		#processing image for prediction
		img = Image.open(image_name)
		img = img.resize((64,63), Image.ANTIALIAS)
		img = ImageOps.invert(img)
		img = np.array(img)
		img = img.reshape(1,63,64,1)

		#making prediction on img given current model
		#TODO make this work for every model.
		classes = model.predict(img)
		indices = np.array([np.argsort(prediction)[:3] for prediction in classes])
		indices = np.ndarray.flatten(indices)
		x = json.load(open('cleaned_radical_jis_utf16_dict', 'r'));
		x = list(x['hiragana'])
		codes = [x[index] for index in indices]
		codeset = set(codes)
		
		#displaying predictions
		file = codecs.open("code_to_hira.json", "r",encoding = "utf8")
		code_to_hira = json.load(file)
		x = []
		s = ""
		for key in codeset:
			s += code_to_hira[key]
		predicted_kanji.insert("0.0", s)
		#re-enabling user input
		os.remove(image_name)
		w.bind("<B1-Motion>", paint)
		w.bind("<B3-Motion>", erase)
		b.config(state="active")

	def paint(event):
	   x, y = (event.x), (event.y)
	   w.create_line(x, y, x + 1, y,width = 8)
	   draw.line([(x, y), (x + 1, y)],fill = "black",width = 8)

	def erase(event):
		x, y = event.x, event.y
		w.create_line(x,y,x+1,y+1, width = 8, color = "white")
		draw.line([(x, y), (x + 1, y)],fill = "white",width = 8)

	w.pack(expand = YES, fill = BOTH)
	w.bind("<B1-Motion>", paint)
	w.bind("<B3-Motion>", erase)
	message = Label(master, text = "Draw with left click, erase with right click. Press \"Predict\" to recieve your character")
	message.pack(side = BOTTOM )
	predicted_kanji = Text(master,height=1, width = 10,highlightcolor= "blue")
	predicted_kanji.pack(side = BOTTOM)
	b = Button(master, text="Predict", command=predict)
	b.pack()
gui_setup()
mainloop()