import sqlite3
import datetime
import sys
from collections import defaultdict

db = sqlite3.connect('GirisCikis.db')
now = datetime.datetime.now()
conn = db.cursor()

tarihBicim = '%d.%m.%Y'
saatBicim = '%H:%M:%S'


def tarih():
    return now.strftime(tarihBicim)
    # '%d' % now.day + '.' + '%d' % now.month + '.' + '%d' % now.year


def saat():
    return now.strftime(saatBicim)
    # '%d' % now.hour + ':' + '%d' % now.minute


def tarih_ekle():
    conn.execute("INSERT INTO veriler (tarih,saat) VALUES (?,?)",
                 (tarih(), saat()))
    db.commit()
    print('Kayıt gerçekleştirildi.')


def veri_yazdir():
    for veri in conn.execute('SELECT tarih,saat FROM veriler'):
        print(veri[0], veri[1])


def sure_hesapla():
    # Dict
    dict_ts = {}
    for veri in conn.execute('SELECT tarih, saat FROM veriler'):
        dict_ts.setdefault(veri[0], []).append(veri[1])

    s_list = []
    for key in dict_ts.values():  # 04:00:00, ... ham günlük toplam süre
        s1 = key[0]
        s2 = key[-1]
        diff = now.strptime(s2, saatBicim) - now.strptime(s1, saatBicim)
        s_list.append(str(diff))
        print(diff)
    print(s_list)

    total = now.strftime(saatBicim)
    for index in s_list:
        total += now.strptime(index, saatBicim)

    print(total)

# TODO: Elle veri ekleme ve silme fonksiyonu ekle
# TODO: database deki saat biçimlerini 00:00:00 şekline getir.

def secenekler():
    print('1 - Giriş kaydı')
    print('2 - Veri ekle')
    print('3 - Verileri yazdır')
    print('4 - Süre hesapla')
    print('5 - Çıkış')


def bosluk():
    print('-------------------\n')


def islemler():
    secenekler()

    try:
        girdi = int(input('>>>'))
    except:
        girdi = 0
        print('Gardaş seçenekler 1 den 5 e kadar. Yapma gözünü seveyim.')

    print()
    if girdi == 1:
        tarih_ekle()
    elif girdi == 2:
        pass
    elif girdi == 3:
        veri_yazdir()
    elif girdi == 4:
        sure_hesapla()
    elif girdi == 5:
        db.close()
        print('Veriler kayıt edildi.')
        print('Çıkmak için Enter a basın.')
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
