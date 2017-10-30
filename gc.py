import sqlite3
import datetime
import sys

# TODO: Database verilerini tarih olarak küçükden büyüğe doğru sırala.
# (Sonradan eskiye dönük tarih eklenmesi durumunda düzgün görülmesi için)

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
saatBicim = '%H:%M:%S'


def tarih():
    return now.strftime(tarihBicim)


def saat():
    return now.strftime(saatBicim)


def ani_ekle():
    conn.execute("INSERT INTO veriler (tarih,saat) VALUES (?,?)",
                 (tarih(), saat()))
    db.commit()
    print('Kayıt gerçekleştirildi.')


def elle_ekle(t, s):
    conn.execute("INSERT INTO veriler (tarih,saat) VALUES (?,?)",
                 (t, s))
    db.commit()


def elle_sil(t, s):
    try:
        conn.execute("DELETE FROM veriler WHERE tarih = ? AND saat = ?",
                     (t, s))
    except SyntaxError:
        print('Eksik veya yanlış girdi.')
    db.commit()


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
        # print('for: sure_hesapla, diff = ' + str(diff))
    # print('s_list = ' + str(s_list))

    total = datetime.datetime.strptime('0:00:00', saatBicim)
    for index in s_list:
        total = total + datetime.timedelta(hours=int(index[:-6]),
                                           minutes=int(index[-5:-3]),
                                           seconds=int(index[-2:]))
        print('index = ' + index)

    print('total = ' + total.strftime(saatBicim))


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

    try:
        girdi = int(input('>>>'))
    except ValueError:
        girdi = 0
        print('Sayı giriniz.')

    if girdi == 1:
        ani_ekle()
    elif girdi == 2:
        elle_ekle(input('Tarih (Örn 01.01.01) : '), input('Saat (Örn 01:01) : '))
    elif girdi == 3:
        elle_sil(input('Tarih (Örn 01.01.01) : '), input('Saat (Örn 01:01) : '))
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


# try:
# input(r"Devam etmek için Enter'a basın...")
# os.system('cls')
# except SyntaxError:
#     pass

while True:
    now = datetime.datetime.now()
    islemler()
    bosluk()

###############################
# Veri güncelleme
###############################
# db.execute("UPDATE veriler SET tarih='25.10.17' WHERE tarih='23.10.17'")
