"""
run:
usage: python train.py --glove_path ./glove.6B/glove.6B.300d.txt \
    --glove_vec glove_vec.pkl \
    --emotion6 C:\data\Emotion6\images \
    --emotion_glove_vec emotion_glove_vec.pkl
"""

from dataset import Dataset
from gloves import emotionGloveToPickle
from keras.layers import Dense, BatchNormalization, Activation, Dropout
from tensorflow.keras.optimizers import Adam
import pickle

from tensorflow.keras.applications.resnet50 import ResNet50
from keras.models import Model
from sklearn.model_selection import train_test_split
import argparse
import os
import keras.backend as K
import numpy as np

def euclidean_distance_loss(y_true, y_pred):
    return K.sqrt(K.sum(K.square(y_pred-y_true), axis=-1))

"""
build model with ResNet50
"""
def build_model():
    base_model=ResNet50(input_shape=(224,224,3))
    for layer in base_model.layers:
        layer.trainable=False
    x=base_model.get_layer('avg_pool').output
    x=Dense(2000)(x)
    x=BatchNormalization()(x)
    x=Activation('relu')(x)
    x=Dropout(0.5)(x)
    x=Dense(300)(x)
    x=BatchNormalization()(x)

    model = Model(base_model.inputs, x)
    
    return model

parser=argparse.ArgumentParser()

parser.add_argument('--glove_path', required=True, help='original path to glove text file')
parser.add_argument('--glove_vec', required=True, help='path to original glove vectors saved in pickle')
parser.add_argument('--emotion6', required=True,help='path to emotion6')
parser.add_argument('--emotion_glove_vec', required=True, help='path \
    to emotion_glove_vec, it contains word vectors with emotion classes in \
        given affective benchmark dataset')

parser.add_argument('--lr', default=0.01, help='learning rate for optimizer')

args=parser.parse_args()

if not os.path.exists(args.emotion_glove_vec):
    emotionGloveToPickle(args)

with open(args.emotion_glove_vec, 'rb') as f: 
    emotionWordToVec=pickle.load(f) #contains semantic embeddings for emotion
    
"""
train model that predicts emotions given an affective image without contextual contents.
The training dataset is emotion6 benchmark
"""

"""
prepare training data
"""

dataset_ob=Dataset()

filepaths=dataset_ob.getFileList(args.emotion6)

X, y = dataset_ob.preprocessInputData(filepaths, emotionWordToVec)

print(X.shape, y.shape)

model = build_model()
adam=Adam(args.lr)
model.compile(loss=euclidean_distance_loss, optimizer=adam, metrics=['accuracy']) 
train_X, val_X, train_y, val_y = train_test_split(X, y, test_size=0.2, random_state=7)
model.fit(train_X, train_y, validation_data=(val_X, val_y), epochs=50, batch_size=30)

model.save('saved_model.h5')










