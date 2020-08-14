import csv, sqlite3
import pandas as pd

con = sqlite3.connect("database.db") 
table_name = 'presence'
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS table_name (Name, first_seen);") 

# df = pd.read_csv('presence.csv')
# print(df.head())
# df.to_sql(table_name, con, if_exists='append', index=False)

with open('presence.csv','r') as fin: 
    dr = csv.DictReader(fin)
    to_db = [(i['Name'], i['first_seen']) for i in dr]
    # print(fin)
    
cur.executemany("INSERT INTO table_name ('Name', 'first_seen') VALUES (?, ?);", to_db)
con.commit()
con.close()