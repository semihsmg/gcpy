import sqlite3
import datetime
import sys

db = sqlite3.connect('GirisCikis.db')
now = datetime.datetime.now()
conn = db.cursor()


def tarih():
    return now.strftime('%d.%m.%Y')  # '%d' % now.day + '.' + '%d' % now.month + '.' + '%d' % now.year


def saat():
    return now.strftime('%H:%M')  # '%d' % now.hour + ':' + '%d' % now.minute


def tarih_ekle():
    conn.execute("INSERT INTO veriler (tarih,saat) VALUES (?,?)",
                 (tarih(), saat()))
    db.commit()
    print('Kayıt gerçekleştirildi.')


def veri_yazdir():
    for veri in conn.execute('SELECT tarih,saat FROM veriler'):
        print(veri[0], veri[1])


def secenekler():
    print('1 - Giriş kaydı')
    print('2 - Veri ekle')
    print('3 - Verileri yazdır')
    print('4 - Süre hesapla')
    print('5 - Çıkış')


def bosluk():
    print('####################\n')


def islemler():
    secenekler()

    try:
        girdi = int(input('>>>'))
    except:
        girdi = 0
        print('Gardaş seçenekler 1 den 4 e kadar. Yapma gözünü seveyim.')

    print()
    if girdi == 1:
        tarih_ekle()
    elif girdi == 2:
        pass
    elif girdi == 3:
        veri_yazdir()
    elif girdi == 4:
        pass
    elif girdi == 5:
        db.close()
        print('Veriler kayıt edildi.')
        print('Çıkmak için herhangi bir tuşa basın.')
        input('')
        sys.exit()


# try:
# input(r"Devam etmek için Enter'a basın...")
# os.system('cls')
# except SyntaxError:
#     pass


while True:
    islemler()
    bosluk()
# ##############################
# # Tablo oluşturma
# ##############################
# db.execute('''CREATE TABLE IF NOT EXISTS
#                   veriler (
#                       tarih VARCHAR(50) NOT NULL,
#                       saat VARCHAR(50) NOT NULL
#                       )''')
# if db:
#     print('Verilere erişildi.')
# else:
#     print('Verilere erişilemedi')
# ##############################
# # Veri ekleme
# ##############################
# db.execute('''INSERT INTO veriler (tarih,saat) VALUES ('25.10.17','16:10')''')
# db.commit()

###############################
# Veri silme
###############################
# db.execute("DELETE FROM veriler WHERE tarih='24.10.17'")

###############################
# Veri güncelleme
###############################
# db.execute("UPDATE veriler SET tarih='25.10.17' WHERE tarih='23.10.17'")

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
