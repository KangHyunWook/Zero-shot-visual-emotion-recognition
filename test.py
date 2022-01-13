"""

"""
from annoy import AnnoyIndex
from keras.models import load_model
from dataset import ArtPhoto
from sklearn.metrics import f1_score

import pickle

def euclidean_distance_loss(y_true, y_pred):
    return K.sqrt(K.sum(K.square(y_pred-y_true), axis=-1))

unseen_emotions=['amusement', 'contentment', 'excitement', 'awe']

model = load_model('saved_model.h5', custom_objects={'euclidean_distance_loss': euclidean_distance_loss})

artphoto_dataset=r'C:\data\artphoto'
dataset_ob=ArtPhoto()

filepaths=dataset_ob.getFileList(artphoto_dataset)

reduced_filepaths=dataset_ob.getFilePathsWithUnseenEmotions(filepaths, unseen_emotions)

with open('emotion_glove_vec.pkl', 'rb') as f:
    emotionWordToVec=pickle.load(f)

X, y = dataset_ob.preprocessInputData(reduced_filepaths, emotionWordToVec)

print(X.shape, y.shape)

emotion_labels=dataset_ob.getEmotionClasses(artphoto_dataset)
print(emotion_labels)

feats=model.predict(X)
print('feats len:', len(feats))
print(feats[0].shape)
aIndex = AnnoyIndex(y.shape[1], metric='euclidean')
for i in range(len(emotion_labels)):
    aIndex.add_item(i, emotionWordToVec[emotion_labels[i]])

aIndex.build(10)

correct=0
y_true=[]
y_pred=[]
for i in range(len(reduced_filepaths)):
    emotion=dataset_ob.getEmotion(reduced_filepaths[i])
    true_idx=emotion_labels.index(emotion)
    nearest_emotion=aIndex.get_nns_by_vector(feats[i], 3)
    print(emotion)
    print(true_idx)
    print(nearest_emotion)
    y_true.append(true_idx)
    y_pred.append(nearest_emotion[0])
    if true_idx==nearest_emotion[0]:
        correct+=1
        
print('acc: ',correct/len(reduced_filepaths))
print('f1-score: ',f1_score(y_true, y_pred, average='weighted'))
    