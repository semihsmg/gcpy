import sqlite3
import datetime
import sys
import re

db = sqlite3.connect("C:/gcpy_db/GirisCikis.db")
conn = db.cursor()
dt = datetime.datetime
file_name = "C:/gcpy_db/calc.txt"
file = open(file_name, "w")

##############################
# Tablo oluşturma
##############################
db.execute('''CREATE TABLE IF NOT EXISTS
                  veriler (
                      date VARCHAR(50) NOT NULL,
                      time VARCHAR(50) NOT NULL
                      )''')
if db:
    print('Verilere erişildi.')
    print()
else:
    print('Verilere erişilemedi')

dateFormat = '%d.%m.%Y'
timeFormat = '%H:%M'  # :%S
timeFormat_with_day = '%d:%H:%M'  # :%S


def date(now):
    return now.strftime(dateFormat)


def time(now):
    return now.strftime(timeFormat)


def user_input_date():
    return input('Tarih (Örn 01.01.2000) : ')


def user_input_time():
    return input('Saat (Örn 01:01) : ')


def regex_time():
    matched = None
    while matched is None:
        s = user_input_time()
        matched = re.match(r'[0-2][0-9]:[0-5][0-9]', s)
        if matched is not None:
            return s
        else:
            print('Saat formatı 00:00 şeklinde olmalı.')


def regex_date():
    matched = None
    while matched is None:
        t = user_input_date()
        matched = re.match(r'((([0][1-9])|([1-2][0-9]))|([3][0-1]))\.(([0][1-9])|([1][0-2]))\.([2]\d\d\d)', t)
        if matched is not None:
            return t
        else:
            print('Tarih formatı 01.01.2000 şeklinde olmalı.')


def record_msg():
    print('Kayıt gerçekleştirildi.')


def add_now(now):
    conn.execute('INSERT INTO veriler (date,time) VALUES (?,?)',
                 (date(now), time(now)))
    db.commit()
    record_msg()


def add_manual():
    conn.execute('INSERT INTO veriler (date,time) VALUES (?,?)',
                 (regex_date(), regex_time()))
    db.commit()
    record_msg()


def user_input_control():
    try:
        return int(input('>>>'))
    except ValueError:
        print('Sayı giriniz.')


def del_manual_secenek():
    print('1 - Belirli tarihden saat sil')
    print('2 - x tarihine sahip bütün kayıtlar')
    print('3 - Ana menü')


def del_manual():
    try:
        move_on = False
        while not move_on:
            del_manual_secenek()
            user_input = user_input_control()
            if user_input == 1:
                conn.execute('DELETE FROM veriler WHERE date = ? AND time = ?',
                             (regex_date(), regex_time()))
            elif user_input == 2:
                conn.execute('DELETE FROM veriler WHERE date = ?', (regex_date(),))
            elif user_input == 3:
                return
            if user_input == (1 or 2):  # or 3
                print('Silme işlemi gerçekleşirildi.')
                move_on = True
            else:
                print('Seçenekler arasında ' + str(user_input) + ' mevcut değil.')
    except ValueError:
        print('Eksik veya yanlış girdi.')
    db.commit()


def dict_ts():
    # Creating dictionary with sorted time values
    dict_raw = {}
    dict_sort = {}
    for veri in conn.execute('SELECT date, time FROM veriler'):
        dict_raw.setdefault(veri[0], []).append(veri[1])
    for i, j in dict_raw.items():
        dict_sort.setdefault(i, sorted(j))

    return dict_sort


def table_time_str(s1, s2):
    return str(s1 + ' > ' + s2)


def table_str(key, table_time, diff):
    info = '{0:12s} {1:15s} {2:7s}'.format(key, table_time, diff)
    print(info)
    file.write(info + '\n')


def difference(s1, s2):
    return dt.strptime(s2, timeFormat) - dt.strptime(s1, timeFormat)


def txt_write(line):
    file.write(line)


def txt_writelines(lines):
    file.writelines(lines)


def calc_time():  # Mesai içinde ve dışında kalan çalışma saatlerini ayrı ayrı hesaplama
    table_title = '{0:12s} {1:15s} {2:7s}'.format('Tarih', 'Saat', 'Süre')
    print(table_title)
    txt_write(table_title + '\n')

    before_1730_list = []
    after_1730_list = []
    time_to_leave = '17:30'
    for key, arr in dict_ts().items():
        if max(arr) <= time_to_leave:
            before_1730_list.append(str(difference(min(arr), max(arr))))
        else:
            before_1730_list.append(str(difference(min(arr), time_to_leave)))
            after_1730_list.append(str(difference(time_to_leave, max(arr))))
        table_str(str(key), table_time_str(min(arr), max(arr)),
                  str(difference(min(arr), max(arr))))

    total_1 = dt.strptime('01:00:00', timeFormat_with_day)
    total_2 = dt.strptime('00:00', timeFormat)
    for index in before_1730_list:
        hrs, mins, secs = index.split(':')
        total_1 = total_1 + datetime.timedelta(days=00, hours=int(hrs),
                                               minutes=int(mins))
    for index in after_1730_list:
        hrs, mins, secs = index.split(':')
        total_2 = total_2 + datetime.timedelta(hours=int(hrs),
                                               minutes=int(mins))
    number_of_days = 'Toplam gün = ' + str(len(dict_ts().keys()))
    d, h, m = str(total_1.strftime(timeFormat_with_day)).split(':')
    shift = 'Toplam mesai = ' + str(int(d) - 1) + ' gün + ' \
            + h + ':' + m + ' = ' + str((((int(d) - 1) * 24) + int(h))) + ':' + m
    extra_shift = 'Toplam fazla mesai = ' + total_2.strftime(timeFormat)
    print('\n' + number_of_days + '\n' + shift + '\n' + extra_shift)

    list_of_calc = ['\n', number_of_days + '\n', shift + '\n', extra_shift + '\n']
    txt_writelines(list_of_calc)

    # s_list = []
    # for key, arr in dict_ts().items():
    #     diff = difference(min(arr), max(arr))
    #     s_list.append(str(diff))
    #     table_str(str(key), table_time_str(min(arr), max(arr)), str(diff))

    # total = dt.strptime('00:00', timeFormat)
    # for index in s_list:
    #     total = total + datetime.timedelta(hours=int(index[:-6]),
    #                                        minutes=int(index[-5:-3]))
    #     # print('index = ' + index)
    # print()
    # print('Toplam gün = ', len(dict_ts().keys()))
    # print('Toplam süre = ' + total.strftime(timeFormat))


def print_data():
    # for veri in conn.execute('SELECT date,time FROM veriler'):
    #     print(veri[0], veri[1])
    for i, j in dict_ts().items():
        print(i, j)  # sorted(j)


def choices():
    print('1 - Giriş kaydı')
    print('2 - Veri ekle')
    print('3 - Veri sil')
    print('4 - Verileri yazdır')
    print('5 - Süre hesapla')
    print('6 - Çıkış')


def exit_app():
    db.close()
    file.close()
    print('Veriler kayıt edildi.')
    print('Çıkmak için Enter a basın.')
    input('')
    sys.exit()


def line():
    print('-------------------')


def operations(now):
    choices()
    user_input = user_input_control()
    print()
    if user_input == 1:
        add_now(now)
    elif user_input == 2:
        add_manual()
    elif user_input == 3:
        del_manual()
    elif user_input == 4:
        print_data()
    elif user_input == 5:
        calc_time()
    elif user_input == 6:
        exit_app()
    else:
        print('Gardaş seçenekler 1 den 6 ya kadar. Yapma gözünü seveyim.')
    print()
    line()

###############################
# Veri güncelleme
###############################

# db.execute("UPDATE veriler SET date='25.10.17' WHERE date='23.10.17'")
