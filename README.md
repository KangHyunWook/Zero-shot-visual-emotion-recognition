# Zeroshot-visual-emotion-recognition
<h2>Project descriptions</h2>
The model is trained with 6 basic emotions(anger, disgust, fear, joy, sadness, surprise) <br />
Through zero-shot learning, the model is capable of predicting unseen emotions not included in the training set, which are amusement, awe, excitement, contentment<br />

<h2>Dataset Download links</h2>
glove.6B.zip: https://nlp.stanford.edu/projects/glove/ <br />
emotion6: http://chenlab.ece.cornell.edu/downloads.html <br />
artphoto: https://www.imageemotion.org/ <br />


<h2>How to train</h2> python train.py --glove_path ./glove.6B/glove.6B.300d.txt \ <br />
                    --glove_vec glove_vec.pkl \<br />
                    --emotion6 C:\data\Emotion6\images \<br />
                    --emotion_glove_vec emotion_glove_vec.pkl

<h2>Predict unseen emotions</h2>
python test.py --artphoto C:/data/artphoto
