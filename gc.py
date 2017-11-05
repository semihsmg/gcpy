import sqlite3
import datetime
import sys
import re

# TODO: Database verilerini tarih - saat olarak küçükden büyüğe doğru sırala.

db = sqlite3.connect('GirisCikis.db')
conn = db.cursor()

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

tarihBicim = '%d.%m.%Y'
saatBicim = '%H:%M'  # :%S


def tarih():
    return now.strftime(tarihBicim)


def saat():
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
        matched = re.match(r'((([0]?[1-9])|([1-2][0-9]))|([3][0-1]))\.(([0]?[1-9])|([1][0-2]))\.([2]\d\d\d)', t)
        if matched is not None:
            return t
        else:
            print('Tarih formatı 01.01.2000 şeklinde olmalı.')


def ani_ekle():
    conn.execute('INSERT INTO veriler (tarih,saat) VALUES (?,?)',
                 (tarih(), saat()))
    db.commit()
    print('Kayıt gerçekleştirildi.')


def elle_ekle():
    conn.execute('INSERT INTO veriler (tarih,saat) VALUES (?,?)',
                 (regex_tarih(), regex_saat()))
    db.commit()


def girdi_kontrol():
    try:
        return int(input('>>>'))
    except ValueError:
        print('Sayı giriniz.')


def elle_sil_secenek():
    print('1 - Belirli tarih ve saat')
    print('2 - x tarihine sahip bütün kayıtlar')
    print('3 - x saatine sahip bütün kayıtlar')


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
    except ValueError:
        print('Eksik veya yanlış girdi.')

    print('Silme işlemi gerçekleşirildi.')
    db.commit()


def veri_yazdir():
    for veri in conn.execute('SELECT tarih,saat FROM veriler'):
        print(veri[0], veri[1])


def dict_ts():
    # Dictionary with unsorted values
    dict_raw = {}
    for veri in conn.execute('SELECT tarih, saat FROM veriler'):
        dict_raw.setdefault(veri[0], []).append(veri[1])
    return dict_raw


def sure_hesapla():
    #  den önce ve sonrası için ayrı ayrı saat çıktısı
    # s_list = []
    # for arr in dict_ts().values():
    #     sorted_arr = sorted(arr)
    #     for s in sorted_arr:
    #         if s <= '05:00':

    s_list = []
    # hergünün arrayinden max ve min saati bul ve birbirinden çıkartıp s_list e koyar
    for arr in dict_ts().values():
        s1 = min(arr)  # arr[0]
        s2 = max(arr)  # arr[-1]
        # print('Array min max: ' + s1 + ' - ' + s2)
        diff = now.strptime(s2, saatBicim) - now.strptime(s1, saatBicim)
        s_list.append(str(diff))
        # print('for: sure_hesapla, diff = ' + str(diff))
    # print('s_list = ' + str(s_list))

    total = datetime.datetime.strptime('0:00', saatBicim)  # :00
    for index in s_list:
        total = total + datetime.timedelta(hours=int(index[:-6]),
                                           minutes=int(index[-5:-3]),
                                           seconds=int(index[-2:]))
        # print('index = ' + index)

    print('Total time = ' + total.strftime(saatBicim))


def secenekler():
    print('1 - Giriş kaydı')
    print('2 - Veri ekle')
    print('3 - Veri sil')
    print('4 - Verileri yazdır')
    print('5 - Süre hesapla')
    print('6 - Çıkış')


def bosluk():
    print('-------------------')


def islemler():
    secenekler()

    girdi = girdi_kontrol()
    # try:
    #     girdi = int(input('>>>'))
    # except ValueError:
    #     girdi = 0
    #     print('Sayı giriniz.')

    if girdi == 1:
        ani_ekle()
    elif girdi == 2:
        elle_ekle()
    elif girdi == 3:
        elle_sil()
    elif girdi == 4:
        veri_yazdir()
    elif girdi == 5:
        sure_hesapla()
    elif girdi == 6:
        db.close()
        print('Veriler kayıt edildi.')
        print('Çıkmak için Enter a basın.')
        input('')
        sys.exit()
    else:
        print('Gardaş seçenekler 1 den 6 e kadar. Yapma gözünü seveyim.')
    bosluk()


# try:
# input(r"Devam etmek için Enter'a basın...")
# os.system('cls')
# except SyntaxError:
#     pass

while True:
    now = datetime.datetime.now()
    islemler()

    ###############################
    # Veri güncelleme
    ###############################

    # db.execute("UPDATE veriler SET tarih='25.10.17' WHERE tarih='23.10.17'")
