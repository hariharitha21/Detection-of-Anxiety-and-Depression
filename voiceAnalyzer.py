# loading json and creating model
from keras.models import model_from_json
import os
import pandas as pd
import librosa
import glob 
import numpy as np
from sklearn.preprocessing import LabelEncoder
def alalyzer():
    lb = LabelEncoder()
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("saved_models/Emotion_Voice_Detection_Model.h5")
    print("Loaded model from disk")

    X, sample_rate = librosa.load('output10.wav', res_type='kaiser_fast',duration=2.5,sr=22050*2,offset=0.5)
    sample_rate = np.array(sample_rate)
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=13),axis=0)
    featurelive = mfccs
    livedf2 = featurelive
    livedf2= pd.DataFrame(data=livedf2)
    livedf2 = livedf2.stack().to_frame().T
    twodim= np.expand_dims(livedf2, axis=2)
    livepreds = loaded_model.predict(twodim, 
                            batch_size=32, 
                            verbose=1)

    livepreds1=livepreds.argmax(axis=1)
    liveabc = livepreds1.astype(int).flatten()
    pl = ["Male Angry","Male Calm","Male Anxious","Male Happy","Male Depressed","Female Angry","Female Calm","Female Anxious","Female Happy","Female Depressed"]
    return pl[int(liveabc)]
