# Zeroshot-visual-emotion-recognition

download links: <br />
glove.6B.zip: https://nlp.stanford.edu/projects/glove/ <br />
emotion6: http://chenlab.ece.cornell.edu/downloads.html <br />
artphoto: https://www.imageemotion.org/ <br />


<h2>How to train</h2> python train.py --glove_path ./glove.6B/glove.6B.300d.txt \ <br />
                    --glove_vec glove_vec.pkl \<br />
                    --emotion6 C:\data\Emotion6\images \<br />
                    --emotion_glove_vec emotion_glove_vec.pkl

<h2>Predict unseen emotions</h2>
