import sqlite3, time

db = sqlite3.connect('GirisCikis.db')

if db:
    print('içerideyim...')

conn = db.cursor()


###############################
# Tablo oluşturma
###############################
# select.execute('''CREATE TABLE IF NOT EXISTS
#                   veriler (
#                       tarih VARCHAR(50) NOT NULL
#                       saat VARCHAR(50) NOT NULL
#                       )''')

###############################
# Veri ekleme
###############################
# select.execute('''INSERT INTO veriler (tarih,saat) VALUES ('25.10.17','16:10')''')

def TarihEkle():
    conn.execute("INSERT INTO veriler (tarih,saat) VALUES (?,?)",
                 (time.time(), time.clock()))
    db.commit()


###############################
# Veri silme
###############################
# select.execute("DELETE FROM veriler WHERE tarih='24.10.17'")

###############################
# Veri güncelleme
###############################
# select.execute("UPDATE veriler SET tarih='25.10.17' WHERE tarih='23.10.17'")


###############################
# [('23.10.17', '16:10'), ... ]
###############################
# read = select.execute('SELECT * FROM veriler')
# print(read.fetchall())

###############################
# Tarih: 00.00.00 Saat: 00:00
###############################
# read = select.execute('SELECT tarih,saat FROM veriler')
# for veri in read.fetchall():
#     print('Tarih: %s - Saat: %s' % veri)

###############################
# 00.00.00 00:00
###############################

TarihEkle()
for veri in conn.execute('SELECT tarih,saat FROM veriler'):
    print(veri[0], veri[1])

db.close()
