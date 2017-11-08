import sqlite3
import datetime
import sys
import re

db = sqlite3.connect("C:/gcpy_db/GirisCikis.db")
conn = db.cursor()
dt = datetime.datetime

##############################
# Tablo oluşturma
##############################
db.execute('''CREATE TABLE IF NOT EXISTS
                  veriler (
                      tarih VARCHAR(50) NOT NULL,
                      saat VARCHAR(50) NOT NULL
                      )''')
if db:
    print('Verilere erişildi.')
    print()
else:
    print('Verilere erişilemedi')

tarihBicim = '%d.%m.%Y'
saatBicim = '%H:%M'  # :%S


def tarih(now):
    return now.strftime(tarihBicim)


def saat(now):
    return now.strftime(saatBicim)


def input_tarih():
    return input('Tarih (Örn 01.01.2000) : ')


def input_saat():
    return input('Saat (Örn 01:01) : ')


def regex_saat():
    matched = None
    while matched is None:
        s = input_saat()
        matched = re.match(r'[0-2][0-9]:[0-5][0-9]', s)
        if matched is not None:
            return s
        else:
            print('Saat formatı 00:00 şeklinde olmalı.')


def regex_tarih():
    matched = None
    while matched is None:
        t = input_tarih()
        matched = re.match(r'((([0][1-9])|([1-2][0-9]))|([3][0-1]))\.(([0][1-9])|([1][0-2]))\.([2]\d\d\d)', t)
        if matched is not None:
            return t
        else:
            print('Tarih formatı 01.01.2000 şeklinde olmalı.')


def kayit_msg():
    print('Kayıt gerçekleştirildi.')


def ani_ekle(now):
    conn.execute('INSERT INTO veriler (tarih,saat) VALUES (?,?)',
                 (tarih(now), saat(now)))
    db.commit()
    kayit_msg()


def elle_ekle():
    conn.execute('INSERT INTO veriler (tarih,saat) VALUES (?,?)',
                 (regex_tarih(), regex_saat()))
    db.commit()
    kayit_msg()


def girdi_kontrol():
    try:
        return int(input('>>>'))
    except ValueError:
        print('Sayı giriniz.')


def elle_sil_secenek():
    print('1 - Belirli tarih ve saat')
    print('2 - x tarihine sahip bütün kayıtlar')
    print('3 - x saatine sahip bütün kayıtlar')
    print('4 - Ana menü')


def elle_sil():
    try:
        elle_sil_secenek()
        girdi = girdi_kontrol()
        if girdi == 1:
            conn.execute('DELETE FROM veriler WHERE tarih = ? AND saat = ?',
                         (regex_tarih(), regex_saat()))
        elif girdi == 2:
            conn.execute('DELETE FROM veriler WHERE tarih = ?', (regex_tarih(),))
        elif girdi == 3:
            conn.execute('DELETE FROM veriler WHERE saat = ?', (regex_saat(),))
        elif girdi == 4:
            return
        if girdi == 1 or 2 or 3:
            print('Silme işlemi gerçekleşirildi.')
    except ValueError:
        print('Eksik veya yanlış girdi.')
    db.commit()


def dict_ts():
    # Dictionary with unsorted values
    dict_raw = {}
    for veri in conn.execute('SELECT tarih, saat FROM veriler'):
        dict_raw.setdefault(veri[0], []).append(veri[1])
    return dict_raw


def difference(s1, s2):
    return dt.strptime(s2, saatBicim) - dt.strptime(s1, saatBicim)


def sure_hesapla():
    print('{0:12s} {1:15s} {2:7s}'.format('Tarih', 'Saat', 'Süre'))

    s_list = []
    for key, arr in dict_ts().items():
        diff = difference(min(arr), max(arr))
        max_min_saat = min(arr) + ' > ' + max(arr)
        print('{0:12s} {1:15s} {2:7s}'
              .format(str(key), str(max_min_saat), str(diff)))
        s_list.append(str(diff))

    total = dt.strptime('0:00', saatBicim)
    for index in s_list:
        total = total + datetime.timedelta(hours=int(index[:-6]),
                                           minutes=int(index[-5:-3]))
        # print('index = ' + index)
    print()
    print('Toplam süre = ' + total.strftime(saatBicim))


def veri_yazdir():
    # for veri in conn.execute('SELECT tarih,saat FROM veriler'):
    #     print(veri[0], veri[1])
    for i, j in dict_ts().items():
        print(i, sorted(j))


def secenekler():
    print('1 - Giriş kaydı')
    print('2 - Veri ekle')
    print('3 - Veri sil')
    print('4 - Verileri yazdır')
    print('5 - Süre hesapla')
    print('6 - Çıkış')


def cikis():
    db.close()
    print('Veriler kayıt edildi.')
    print('Çıkmak için Enter a basın.')
    input('')
    sys.exit()


def bosluk():
    print('-------------------')


def islemler(now):
    secenekler()
    girdi = girdi_kontrol()
    print()
    if girdi == 1:
        ani_ekle(now)
    elif girdi == 2:
        elle_ekle()
    elif girdi == 3:
        elle_sil()
    elif girdi == 4:
        veri_yazdir()
    elif girdi == 5:
        sure_hesapla()
    elif girdi == 6:
        cikis()
    else:
        print('Gardaş seçenekler 1 den 6 ya kadar. Yapma gözünü seveyim.')
    print()
    bosluk()


    ###############################
    # Veri güncelleme
    ###############################

    # db.execute("UPDATE veriler SET tarih='25.10.17' WHERE tarih='23.10.17'")
