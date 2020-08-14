import sqlite3 as db
import os
import sys


class Image(object):
    def __init__(self):
        self.images = []

    def load_dir(self, path='../images_for_timeframe'):

        for x in os.listdir(path):
            self.images.append(x)

        return self.images

    def create_db(self, name, image):
        connection = db.connect("../venv/images.db")
        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS DataBase (name TEXT, images BLOB)
        """)

        cursor.execute("""
        INSERT INTO DataBase (name , images ) VALUES (?,?)
        """, (name,image))

        connection.commit()
        cursor.close()
        connection.close()


def fetch_data():
    conter = 1
    os.chdir("../venv")
    connection = db.connect("images.db")
    cursor = connection.cursor()

    os.chdir("../venv")

    #data

def main():
    obj = Image()
    os.chdir("../images_for_timeframe")
    print(obj.load_dir())

    for x in obj.load_dir():
        with open(x, "rb") as f:
            data = f.read()
            obj.create_db(name=x, image=data)
            print("{} added to db".format(x))


if __name__ == "__main__":
    main()
