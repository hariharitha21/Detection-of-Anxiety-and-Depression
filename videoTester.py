import os
import cv2
import numpy as np
from keras.models import model_from_json
from keras.preprocessing import image
def exp():
    #load model
    model = model_from_json(open("fer.json", "r").read())
    #load weights
    model.load_weights('fer.h5')


    face_haar_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


    cap=cv2.VideoCapture(0)
    count_anx=0
    count_desp=0
    count_normal=0

    while True:
        ret,test_img=cap.read()# captures frame and returns boolean value and captured image
        if not ret:
            continue
        gray_img= cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)

        faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.32, 5)


        for (x,y,w,h) in faces_detected:
            cv2.rectangle(test_img,(x,y),(x+w,y+h),(255,0,0),thickness=3)
            roi_gray=gray_img[y:y+w,x:x+h]#cropping region of interest i.e. face area from  image
            roi_gray=cv2.resize(roi_gray,(48,48))
            img_pixels = image.img_to_array(roi_gray)
            img_pixels = np.expand_dims(img_pixels, axis = 0)
            img_pixels /= 255 #normalizing

            predictions = model.predict(img_pixels)

            #find max indexed array
            max_index = np.argmax(predictions[0])

            emotions = ('angry', 'disgust', 'Anxiety', 'happy', 'Depressed', 'surprise', 'neutral')
            predicted_emotion = emotions[max_index]
            if predicted_emotion=='Anxiety':
                count_anx=count_anx+1
            elif predicted_emotion=='Depressed':
                count_desp=count_desp+1
            else:
                count_normal=count_normal+1
            cv2.putText(test_img, predicted_emotion, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        resized_img = cv2.resize(test_img, (1000, 700))
        
        cv2.imshow('Facial emotion analysis ',resized_img)
        cv2.setWindowProperty("Facial emotion analysis ", cv2.WND_PROP_TOPMOST, 1)

        



        if cv2.waitKey(10) == ord('q'):#wait until 'q' key is pressed
            if count_anx>count_desp:
                if count_anx>count_desp:
                    res='Anxious'
                else:
                    res='Normal'
            else:
                if count_normal>count_desp:
                    res='Normal'
                else:
                    res='Depressed'
            return res
            break

    cap.release()
    cv2.destroyAllWindows