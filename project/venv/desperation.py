import numpy as np
import cv2
import face_recognition
import os
from datetime import datetime
import csv, sqlite3
from sqlite3 import Error



TABLE_NAME = 'presence'

def encode_images(list_of_images):
    encoded_list = []
    for image in list_of_images:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encoded_image = face_recognition.face_encodings(image)[0]
        encoded_list.append(encoded_image)
    return encoded_list

def store_names_and_time(name, conn):
    # We can link this to a database
    database = './database/date.db'
    conn = create_connection(database)
    cur = conn.cursor()

    table_name = 'presence'
    with open('presence.csv', 'r+') as f: #r+ is for both reading and writing, you don't need to google dumdum
        data_list = f.readlines()
        names = []
        # print(data_list)
        for line in data_list:
            entry = line.split(',')
            names.append(entry[0]) #that's the name
        if name not in names:
            now = datetime.now()
            datetime_string = now.strftime('%Y/%m/%d %H:%M:%S')
            f.writelines(f'\n{name},{datetime_string}')
            # Sending to db
            person = (name, datetime_string)
            create_db(name, datetime_string)

# Database stuff

def create_connection(db_file):

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn
def create_db(name, datetime_string):
    database = './database/date_time.db'
    conn = create_connection(database)

    table_name = 'presence'
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO DataBase (name , time ) VALUES (?,?)
    """, (name,datetime_string))


    conn.commit()
    cur.close()
    conn.close()
def add_person(conn, person):
    database = './database/date_time.db'
    conn = create_connection(database)

    table_name = 'presence'

    sql = ''' INSERT INTO table_name(name,first_seen)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, person)
    conn.commit()
    return cur.lastrowid


def main():
# DB setup
    
    database = './database/date_time.db'
    conn = create_connection(database)

    table_name = 'presence'
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS presence (name TEXT, first_seen TEXT);") 
    # Face recognition stuff

    path = '../images_for_timeframe'
    images = []
    class_names = []
    list_of_images = os.listdir(path) 

    for img_name in list_of_images:
        current_image = cv2.imread(f'{path}/{img_name}')
        images.append(current_image)
        class_names.append(os.path.splitext(img_name)[0])

    encode_list_for_known_images = encode_images(images)

    cap = cv2.VideoCapture(0)

    while True:
        success, image = cap.read()

        image_small = cv2.resize(image, (0,0), None, 0.25,0.25)

        image_small = cv2.cvtColor(image_small, cv2.COLOR_BGR2RGB)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break


        faces_in_current_frame = face_recognition.face_locations(image_small)
        encode_current_frame = face_recognition.face_encodings(image_small, faces_in_current_frame)

        for encoded_face, face_location in zip(encode_current_frame, faces_in_current_frame):
            matches = face_recognition.compare_faces(encode_list_for_known_images, encoded_face) # compare each face with all known faces
            face_distance = face_recognition.face_distance(encode_list_for_known_images, encoded_face) # Gives value of distance of encoded face from each known face

            match_index = np.argmin(face_distance)

            if matches[match_index]:
                name = class_names[match_index].upper()

                y1,x2,y2,x1 = face_location
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                
                cv2.rectangle(image, (x1,y1), (x2,y2), (0,255,0))
                cv2.rectangle(image, (x1,y2-35), (x2,y2), (0,255,0), cv2.FILLED)
                cv2.putText(image, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)

                store_names_and_time(name, conn)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

        cv2.imshow('webcam', image)
        cv2.waitKey(1)

if __name__ == '__main__':

    main()