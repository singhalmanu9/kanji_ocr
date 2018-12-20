# kanji_ocr

A project to read handwritten kanji (Chinese), hiragana, and katakana characters for computers. Began development during Cal Hacks 2018. 

##Model
The optical character recognition model will be comprised of many smaller submodels.
Each submodel will be predicting on a subset of all Japanese characters based on radicals, hiragana, and katakana. Consequently, when an image is passed into a model where its respective character is not present (i.e. if 'あ' is passed into any of the kanji classification submodels), it is marked with the 'OOV' (out of vocabulary) tag. The subsets of kanji that will be trained on are present within the radkfile (see redistribution rights).
##Prediction
For each model, the most-likely character will be outputted and displayed to a user in a list sorted by highest probability within its model (i.e. if one character is predicted within its model with a score of .9, it will be put earlier in the list than a character with a score of .8). Only unique predictions will be shown, so if two models predict the same character, the character will only appear once.
#####Database comes from Electrotechnical Lab (http://etlcdb.db.aist.go.jp). 
