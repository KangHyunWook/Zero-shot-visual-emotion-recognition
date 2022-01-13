from keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input

import os
import numpy as np

class Dataset:
    def __init__(self):
        pass
        
    def getEmotion(self, filepath):
        return filepath.split('\\')[-2]
    
    def getEmotionClasses(self, root):
        emotion_labels=os.listdir(root)
        return sorted(emotion_labels)
    
    def getFileList(self, root):
        items = os.listdir(root)
        pathList=[]
        for item in items:
            full_path=os.path.join(root, item)
            if os.path.isfile(full_path):
                pathList.append(full_path)
            else:
                pathList+=self.getFileList(full_path)
        return pathList

    def preprocessInputData(self, filepaths, emotionWordToVec):
        X=[]
        y=[]
        print('dataset len:', len(filepaths))
        for file in filepaths:
            img = image.load_img(file, target_size=(224,224))
            img = image.img_to_array(img)
            img = preprocess_input(img)
            emotion=self.getEmotion(file)
            sem_rep=emotionWordToVec[emotion]
            X.append(img)
            y.append(sem_rep)
        
        return np.array(X), np.array(y)

class ArtPhoto(Dataset):
    def getEmotion(self, file):
        return file.split('\\')[-1].split('_')[0]
        
    def getEmotionClasses(self, root):
        filenameList=os.listdir(root)
        emotion_set=set()
        for fn in filenameList:
            splits=fn.split('_')
            emotion_set.add(splits[0])
        
        return list(sorted(emotion_set))
    
    def getFilePathsWithUnseenEmotions(self, filepaths, unseen_emotions):
        reduced_filepaths=[]
        for fpth in filepaths:
            emotion = self.getEmotion(fpth)
            if emotion in unseen_emotions:
                reduced_filepaths.append(fpth)
        return reduced_filepaths