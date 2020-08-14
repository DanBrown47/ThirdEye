import sqlite3 as db

connection = db.connect('./database/images.db')

cursor = connection.cursor()


# m = cursor.execute("""
# SELECT * FROM my_table
# """)
# for x in m:
#     print(x[2])



def add_image(name, length):
    with open('/home/swaaz/swaaz/github/the-third-eye-web/project/venv/assets/swaaz/1.png', 'rb') as f:
        m = f.read()
    # print(m)
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS {} (name TEXT, data BLOB)""".format(name))

    sql = """INSERT INTO {} (name, data ) VALUES (?,?)""".format(name)

    cursor.execute(sql, (name, m))

    connection.commit()
    cursor.close()
    connection.close()


def main():
    pass

if __name__ == '__main__':
    main()