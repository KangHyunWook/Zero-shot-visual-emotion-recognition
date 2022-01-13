"""
Description: This program saves emotions in ArtPhoto and Emotion6 affective datasets
            to pickle. All glove vector should have been saved earlier
            
usage: python emotionglovetopickle.py --glove_path ./glove.6B/glove.6B.300d.txt \
    --glove_vec glove_vec.pkl \
    --emotion6 C:\data\Emotion6\images
"""

from dataset import Dataset, ArtPhoto   
import argparse
import os
"""
glove test
"""

"""
load glove_vec.pkl
"""

import numpy as np

def glovetopickle(glove_path):
    cnt=0

    wordToVec={}
    with open(glove_path, 'r', encoding='utf-8') as f:
        for line in f:
            splits=line.split(' ')
            word=splits[0]
            vec=splits[1:]
            wordToVec[word]=np.array(vec,dtype='float32')

       
    for key in wordToVec:
        print(key, wordToVec[key][:5], wordToVec[key].shape)
        cnt+=1
        if cnt>10:
            break

    import pickle 
            
    with open('glove_vec.pkl', 'wb') as f:
        pickle.dump(wordToVec, f, protocol=pickle.HIGHEST_PROTOCOL)
import pickle

"""
Precondition:
    @params:
        emotion6: path to emotion6 dataset. In the original downloaded format:
            ./Emotion6/images
"""
def emotionGloveToPickle(args):
    if not os.path.exists(args.glove_vec):
        glovetopickle(args.glove_path)
        
    with open(args.glove_vec, 'rb') as f:
        wordToVec=pickle.load(f)

    print(len(wordToVec))
    """
    read emotions from dataset
    """
    dataset_ob=Dataset()

    labels=dataset_ob.getEmotionClasses(args.emotion6)
    emotion_set=set(labels)
    dataset_ob=ArtPhoto()
    labels=dataset_ob.getEmotionClasses(r'C:\data\artphoto')
    for label in labels:
        emotion_set.add(label)
        
    print('====emotion_set====')
    print(emotion_set)

    emotionWordToVec={}
    for key in wordToVec:
        if key in emotion_set:
            emotionWordToVec[key]=wordToVec[key]
            
    with open('emotion_glove_vec.pkl', 'wb') as f:
        pickle.dump(emotionWordToVec, f, protocol=pickle.HIGHEST_PROTOCOL)




