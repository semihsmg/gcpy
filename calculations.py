import sqlite3
import datetime
import sys
import re

destination = "C:/gcpy/"

dt = datetime.datetime
this_date = dt.today()

db = sqlite3.connect(destination + str(this_date.month) + "_" + str(this_date.year) + ".db")
conn = db.cursor()
# TODO: txt ve db dosyalrını kendi klasörlerinde tut
# Tablo oluşturma
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
        matched = re.match(r'(([0-1]\d)|([2][0-3])):[0-5]\d', s)
        if matched is not None:
            return s
        else:
            print('Saat formatı 00:00 şeklinde olmalı.')


def regex_date():
    matched = None
    while matched is None:
        t = user_input_date()
        matched = re.match(r'((([0][1-9])|([1-2]\d))|([3][0-1]))\.(([0][1-9])|([1][0-2]))\.([2]\d\d\d)', t)
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


def del_manual_options():
    print('1 - Belirli tarihden saat sil')
    print('2 - x tarihine sahip bütün kayıtlar')
    print('3 - Ana menü')


def del_manual():
    move_on = False
    while not move_on:
        del_manual_options()
        user_input = user_input_control()
        if user_input == 1:
            conn.execute('DELETE FROM veriler WHERE date = ? AND time = ?',
                         (regex_date(), regex_time()))
        elif user_input == 2:
            conn.execute('DELETE FROM veriler WHERE date = ?', (regex_date(),))
        elif user_input == 3:
            return
        if user_input == (1 or 2 or 3):
            if user_input == (1 or 2):
                print('Silme işlemi gerçekleşirildi.')
            move_on = True
        else:
            print('Seçenekler arasında ' + str(user_input) + ' mevcut değil.')

        db.commit()


def update_time_options():
    print("1 - Tarihi değiştir")
    print("2 - Bir tarihdeki saati değiştir")
    print("3 - Ana menü")


def update_time():
    # Veri güncelleme
    # conn.execute("UPDATE veriler SET date='25.10.17' WHERE date='23.10.17'")
    move_on = False
    while not move_on:
        update_time_options()
        user_input = user_input_control()
        deger = user_input
        if user_input == 1:
            # Update date date
            print("Değiştirmek istediğiniz gün:")
            date_d2 = regex_date()
            print("Yeni tarih değeri:")
            date_d1 = regex_date()
            conn.execute("UPDATE veriler SET date = ? WHERE date = ?",
                         (date_d1, date_d2))
        elif user_input == 2:
            # Update specific time of the date
            print("Güncellemeyi yapacağınız gün:")
            date1 = regex_date()
            print("Güncellemek istediğiniz saat:")
            time1 = regex_time()
            print("Yeni saat değeri:")
            time2 = regex_time()
            conn.execute("UPDATE veriler SET time = ? WHERE date = ? AND time = ?",
                         (time2, date1, time1))
        elif user_input == 3:
            return

        if user_input is 1 or 2 or 3:
            if user_input is 1 or 2:
                print('Veri güncelleme gerçekleşirildi.')
            move_on = True
        else:
            print('Seçenekler arasında ' + str(user_input) + ' mevcut değil.')

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


def difference(s1, s2):
    return dt.strptime(s2, timeFormat) - dt.strptime(s1, timeFormat)


def table_str(file, key, table_time, diff):
    info = '{0:12s} {1:15s} {2:7s}'.format(key, table_time, diff)
    print(info)
    file.write(info + '\n')


def txt_write(file, v_line):
    file.write(v_line)


def txt_writelines(file, lines):
    file.writelines(lines)


def calc_time():  # Mesai içinde ve dışında kalan çalışma saatlerini ayrı ayrı hesaplama
    file_name = destination + str(this_date.month) + "_" + str(this_date.year) + ".txt"
    file = open(file_name, "w")

    table_title = '{0:12s} {1:15s} {2:7s}'.format('Tarih', 'Saat', 'Süre')
    print(table_title)
    txt_write(file, table_title + '\n')

    before_1730_list = []
    after_1730_list = []
    time_to_leave = '17:30'
    for key, arr in dict_ts().items():
        min_value = min(arr)
        max_value = max(arr)
        if max_value <= time_to_leave:
            before_1730_list.append(str(difference(min_value, max_value)))
        else:
            before_1730_list.append(str(difference(min_value, time_to_leave)))
            after_1730_list.append(str(difference(time_to_leave, max_value)))
        table_str(file, str(key), table_time_str(min_value, max_value), str(difference(min_value, max_value)))

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
    extra_shift = 'Toplam fazla mesai (15:30 dan sonra) = ' + total_2.strftime(timeFormat)
    print('\n' + number_of_days + '\n' + shift + '\n' + extra_shift)

    list_of_calc = ['\n', number_of_days + '\n', shift + '\n', extra_shift]
    txt_writelines(file, list_of_calc)
    file.close()


def print_data():
    # for veri in conn.execute('SELECT date,time FROM veriler'):
    #     print(veri[0], veri[1])
    for i, j in dict_ts().items():
        print(i, j)  # sorted(j)


def choices():
    print('1 - Giriş kaydı')
    print('2 - Veri ekle')
    print('3 - Veri sil')
    print('4 - Veri Güncelle')
    print('5 - Verileri yazdır')
    print('6 - Süre hesapla')
    print('7 - Çıkış')


def exit_app():
    db.close()
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
        update_time()
    elif user_input == 5:
        print_data()
    elif user_input == 6:
        calc_time()
    elif user_input == 7:
        exit_app()
    else:
        print('Seçenekler 1 den 7 ye kadar. Yapma gözünü seveyim.')
    print()
    line()
