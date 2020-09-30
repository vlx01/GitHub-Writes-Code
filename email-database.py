#This code is for making a database from given text File
#In this sample code I've taken a text file to extract the emails and the number
#of times they appear in text file.
#Ex - From: abc.cdbh@gmail.com
#index of email = 1


import sqlite3

conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('''
CREATE TABLE Counts (email TEXT, count INTEGER)''')

fname = input('Enter file name: ')
try:
    fh = open(fname)
except:
    print('File cannot be opened:', fname)
    exit()

for line in fh:
    if not line.startswith('From: '):
        continue
    pieces = line.split()
    email = pieces[1] #give the index from the text file
    cur.execute('SELECT count FROM Counts WHERE email = ? ', (email,))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (email, count)
                VALUES (?, 1)''', (email,))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE email = ?',
                    (email,))
    conn.commit()

#printing required information
#Here, they are sorted in DESC ORDER
#and information is only asked for top 10 emails
sqlstr = 'SELECT email, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

cur.close()
