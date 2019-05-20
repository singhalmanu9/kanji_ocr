# kanji_ocr

A project to read handwritten kanji (Chinese), hiragana, and katakana characters for computers. Began development during Cal Hacks 2018. 

## Model
The optical character recognition model will be comprised of an initial model and a set of subsequent models.
Each image will be run through at least two models: the initial model and at least one of the subsequent models. The initial model is a predictor of which radicals are present within the character. *N.B. this is where disambiguation between Kanji and Hiragana and Katakana will ideally occur*. 
Once the image has its respective radical (or non-radical) predictions, it will be fed through each of the submodels that were deemed to have their respective radicals present within the image. 

## Prediction
The first model will perform multi-class, multi-label classification. As a result, any label &Psi; above a value &Chi; > .50 will be interpeted as being present within the image. The image will then be fed into each model, &Epsilon;, that corresponds to a valid &Psi;.
### Application
The application that uses this net will select the top three characters from each model and present all of them to the user. Only unique predictions will be shown, so if two models predict the same character, the character will only appear once. The model will also attempt to order each predicted character based on the sum of their scores across all models they scored significantly in. Each character that makes it to the top 3 of any secondary model &Epsilon; will have its score from &Epsilon; added to its previous score from the all secondary models that have run.

## Application Goals
Eventually this OCR system will be implemented into a mobile application within some context. This likely will be done by having the user send the 64x63 image corresponding to their handwriting to a server that has the memory to run the models. Currently, a proof of concept of this application is available in the form of *standalone_predictor.py*.
##### Database comes from Electrotechnical Lab (http://etlcdb.db.aist.go.jp). 
##### The subsets of kanji that will be trained on are present within the radkfile (see redistribution rights).
