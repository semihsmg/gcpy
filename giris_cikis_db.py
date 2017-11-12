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
    print('1 - Belirli tarihden saat sil')
    print('2 - x tarihine sahip bütün kayıtlar')
    print('3 - Ana menü')


def elle_sil():
    try:
        elle_sil_secenek()
        girdi = girdi_kontrol()
        if girdi == 1:
            conn.execute('DELETE FROM veriler WHERE tarih = ? AND saat = ?',
                         (regex_tarih(), regex_saat()))
        elif girdi == 2:
            conn.execute('DELETE FROM veriler WHERE tarih = ?', (regex_tarih(),))
        # elif girdi == 3:
        #     conn.execute('DELETE FROM veriler WHERE saat = ?', (regex_saat(),))
        elif girdi == 3:
            return
        if girdi == 1 or 2:  # or 3
            print('Silme işlemi gerçekleşirildi.')
    except ValueError:
        print('Eksik veya yanlış girdi.')
    db.commit()


def dict_ts():
    # Creating dictionary with sorted time values
    dict_raw = {}
    dict_sort = {}
    for veri in conn.execute('SELECT tarih, saat FROM veriler'):
        dict_raw.setdefault(veri[0], []).append(veri[1])
    for i, j in dict_raw.items():
        dict_sort.setdefault(i, sorted(j))

    return dict_sort


def table_saat_str(s1, s2):
    return str(s1 + ' > ' + s2)


def table_str(key, table_saat, diff):
    print('{0:12s} {1:15s} {2:7s}'.format(key, table_saat, diff))


def difference(s1, s2):
    return dt.strptime(s2, saatBicim) - dt.strptime(s1, saatBicim)


def sure_hesapla():  # Mesai içinde ve dışında kalan çalışma saatlerini ayrı ayrı hesaplama
    print('{0:12s} {1:15s} {2:7s}'.format('Tarih', 'Saat', 'Süre'))

    list_1 = []
    list_2 = []
    mesai_bitis = '17:30'
    for key, arr in dict_ts().items():
        if max(arr) <= mesai_bitis:
            list_1.append(str(difference(min(arr), max(arr))))
        else:
            list_1.append(str(difference(min(arr), mesai_bitis)))
            list_2.append(str(difference(mesai_bitis, max(arr))))
        table_str(str(key), table_saat_str(min(arr), max(arr)), str(difference(min(arr), max(arr))))

    print('l1', list_1)
    print('l2', list_2)

    # TODO: total değerlerine arıyetten days propety de eklemeli çünkü toplam saat 23:59 u geçtikten sonra saat kısmına gün değerini girip dakikaya da saat girioyor.

    total_1 = dt.strptime('00:00', saatBicim)
    total_2 = dt.strptime('00:00', saatBicim)
    for index in list_1:
        hrs, mins, secs = index.split(':')
        total_1 = total_1 + datetime.timedelta(days=0, hours=int(hrs),
                                               minutes=int(mins))
    for index in list_2:
        hrs, mins, secs = index.split(':')
        total_2 = total_2 + datetime.timedelta(days=0, hours=int(hrs),
                                               minutes=int(mins))
    print()
    print('Toplam gün = ', len(dict_ts().keys()))
    print('Toplam mesai = ' + total_1.strftime(saatBicim))
    print('Toplam fazla mesai = ' + total_2.strftime(saatBicim))

    # s_list = []
    # for key, arr in dict_ts().items():
    #     diff = difference(min(arr), max(arr))
    #     s_list.append(str(diff))
    #     table_str(str(key), table_saat_str(min(arr), max(arr)), str(diff))

    # total = dt.strptime('00:00', saatBicim)
    # for index in s_list:
    #     total = total + datetime.timedelta(hours=int(index[:-6]),
    #                                        minutes=int(index[-5:-3]))
    #     # print('index = ' + index)
    # print()
    # print('Toplam gün = ', len(dict_ts().keys()))
    # print('Toplam süre = ' + total.strftime(saatBicim))


def veri_yazdir():
    # for veri in conn.execute('SELECT tarih,saat FROM veriler'):
    #     print(veri[0], veri[1])
    for i, j in dict_ts().items():
        print(i, j)  # sorted(j)


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
