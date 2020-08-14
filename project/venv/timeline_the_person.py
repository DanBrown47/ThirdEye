'''
This file will store the time at which the person was detected
'''

import numpy as np
import cv2
import face_recognition
import os
from datetime import datetime

'''
We just need to add more images of people and the model will work on its own.
'''

path = '../images_for_timeframe'
images = []
class_names = []
list_of_images = os.listdir(path) #gives us the list of names. We will use those names to import the images 1 by 1

# print(list_of_images) # Gives all images with extension

for img_name in list_of_images:
    current_image = cv2.imread(f'{path}/{img_name}')
    images.append(current_image)
    class_names.append(os.path.splitext(img_name)[0]) #get the name without the extension
    # We can put each image in their respective folders and then get the image and then folder name
    # That will be easier to run it through a dataset
# print(class_names) #gives all image names rn, we will use it as our label set
def encode_images(list_of_images):
    encoded_list = []
    for image in list_of_images:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encoded_image = face_recognition.face_encodings(image)[0]
        encoded_list.append(encoded_image)
    return encoded_list

def store_names_and_time(name):
    # We can link this to a database
    with open('presence.csv', 'r+') as f: #r+ is for both reading and writing, you don't need to google dumdum
        data_list = f.readlines()
        names = []
        # print(data_list)
        for line in data_list:
            entry = line.split(',')
            names.append(entry[0]) #that's the name
        if name not in names:
            now = datetime.now()
            datetime_string = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{datetime_string}')

encode_list_for_known_images = encode_images(images)
# print(len(encode_list_for_known_images))
# Since the above command takes time, we will just leave it as is.

'''
get images from webcam
'''
cap = cv2.VideoCapture(0)

while True:
    success, image = cap.read()

    image_small = cv2.resize(image, (0,0), None, 0.25,0.25)
    # (0,0) as we don't want to define any pixel size
    # 0.25,0.25 is the scale, image will be 1/4 the size
    #   * We are doing that because a larger image will take longer to process. Plus, i just have a 1060.
    # We can get the image from swasthik's jetson, we'll look into that
    image_small = cv2.cvtColor(image_small, cv2.COLOR_BGR2RGB)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break


    faces_in_current_frame = face_recognition.face_locations(image_small)
    encode_current_frame = face_recognition.face_encodings(image_small, faces_in_current_frame)
    # We may find multiplefaces in the webcam.
    # For that we will find the location of our faces and then send in the locations to our
    # We take all the faces, encode them and then send in all the locations of all the faces

    # We will not find the matches.
    # We will iterate through all the faces we have found in our current frame
    # And compare all the faces with  all the encodings.
    for encoded_face, face_location in zip(encode_current_frame, faces_in_current_frame):
        matches = face_recognition.compare_faces(encode_list_for_known_images, encoded_face) # compare each face with all known faces
        face_distance = face_recognition.face_distance(encode_list_for_known_images, encoded_face) # Gives value of distance of encoded face from each known face
        # The lowest distance will be our best match.
        # print(face_distance)
        match_index = np.argmin(face_distance)

        if matches[match_index]:
            name = class_names[match_index].upper()
            # print(name)

            y1,x2,y2,x1 = face_location
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            # We multiplied everything by 4 because we had initially scaled our image down to 1/4 the size. If we dont, the prints will be weird
            cv2.rectangle(image, (x1,y1), (x2,y2), (0,255,0))
            cv2.rectangle(image, (x1,y2-35), (x2,y2), (0,255,0), cv2.FILLED)
            cv2.putText(image, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
            # I put the explanations for puttext in the other file ffs, go look over there -_-

            store_names_and_time(name)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
            # This will store the name and time when the face appears

    cv2.imshow('webcam', image)
    cv2.waitKey(1)
