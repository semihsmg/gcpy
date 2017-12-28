import sqlite3
import datetime
import sys
import re
import pathlib

# datetime instance
dt = datetime.datetime
# Return the current local date to this_date
this_date = dt.today()

# Destination of the files
destination = 'C:/gcpy'
file_name = str(this_date.month) + '_' + str(this_date.year)
folder_name = destination + '/' + file_name + '/'
pathlib.Path(folder_name).mkdir(parents=True, exist_ok=True)

# access (or create) database file '{month}_{year}.db'
db = sqlite3.connect(folder_name + file_name + '.db')
conn = db.cursor()

# Create table if not exist in the database file
db.execute('''CREATE TABLE IF NOT EXISTS
                  veriler (
                      date VARCHAR(50) NOT NULL,
                      time VARCHAR(50) NOT NULL
                      )''')
if db:
    print('Verilere erişildi. (Accessed data.)')
    print()
else:
    print('Verilere erişilemedi. (Unable to access data.)')

# date format as day.month.year
dateFormat = '%d.%m.%Y'
# time format as 24 hr base Hour:Minutes
timeFormat = '%H:%M'  # :%S
# For time addition in the time calculation function because date object resets itself after 23:59
timeFormat_with_day = '%d:%H:%M'  # :%S


# get the date of now
def date(now):
    return now.strftime(dateFormat)


# get the time of now
def time(now):
    return now.strftime(timeFormat)


# input function for date
def user_input_date():
    return input('Tarih\Date (01.01.2000) : ')


# input function for time
def user_input_time():
    return input('Saat\Time (01:01) : ')


# Validating time input with regular expression
def regex_date():
    matched = None
    while matched is None:
        t = user_input_date()
        matched = re.match(r'((([0][1-9])|([1-2]\d))|([3][0-1]))\.(([0][1-9])|([1][0-2]))\.([2]\d\d\d)', t)
        if matched is not None:
            return t
        else:
            print('Tarih girişi 01.01.2000 şeklinde olmalı.\nDate input need to be in this (01.01.2000) form.')


# Validating time input with regular expression
def regex_time():
    matched = None
    while matched is None:
        s = user_input_time()
        matched = re.match(r'(([0-1]\d)|([2][0-3])):[0-5]\d', s)
        if matched is not None:
            return s
        else:
            print('Saat formatı 00:00 şeklinde olmalı.\nTime input need to be in this (00:00) form.')


# Record message
def record_msg():
    print('Kayıt gerçekleştirildi \ Recorded')


# Add a date and time instance to the database file of this moment
def add_now(now):
    conn.execute('INSERT INTO veriler (date,time) VALUES (?,?)',
                 (date(now), time(now)))
    db.commit()
    record_msg()


# Add a date and time record to the database file with user input
def add_manual():
    conn.execute('INSERT INTO veriler (date,time) VALUES (?,?)',
                 (regex_date(), regex_time()))
    db.commit()
    record_msg()


# Get the user input and check whether is number or not
def user_input_control():
    try:
        return int(input('>>>'))
    except ValueError:
        print('Sayı giriniz. \ Enter a number please.')


# Manual deletion options
def del_manual_options():
    print('1 - Belirli tarihden saat sil \ Delete time from specific date')
    print('2 - x tarihine sahip bütün kayıtlar \ Delete all record from specific date')
    print('3 - Ana menü \ Main menu')


# Manual delete function
def del_manual():
    # move_on checks while loop is done correctly
    move_on = False
    while not move_on:
        del_manual_options()
        user_input = user_input_control()
        if user_input == 1:
            # delete a specific time from a date
            conn.execute('DELETE FROM veriler WHERE date = ? AND time = ?',
                         (regex_date(), regex_time()))
        elif user_input == 2:
            # delete the key value from dictionary and this means delete all time values (time array)
            conn.execute('DELETE FROM veriler WHERE date = ?', (regex_date(),))
        elif user_input == 3:
            # main menu
            return
        if user_input == (1 or 2 or 3):
            if user_input == (1 or 2):
                print('Silme işlemi gerçekleşirildi. \ Deletion is done')
            move_on = True
        else:
            print('Seçenekler arasında ' + str(user_input) + ' mevcut değil.'
                                                             '\nThere is not ' + str(user_input) + ' as an option')

        db.commit()


# Update time options
def update_date_time_options():
    print('1 - Tarihi değiştir \ Update date')
    print('2 - Bir tarihdeki saati değiştir \ Update a time from specific date')
    print('3 - Ana menü \ Main menu')


# Update date and time function
def update_date_time():
    # move_on checks while loop is done correctly
    move_on = False
    while not move_on:
        update_date_time_options()
        user_input = user_input_control()
        if user_input == 1:
            # Update date
            print('Güncellemek istediğiniz gün \ Date you want to update:')
            date_d2 = regex_date()
            print('Yeni tarih değeri \ New date value:')
            date_d1 = regex_date()
            conn.execute('UPDATE veriler SET date = ? WHERE date = ?',
                         (date_d1, date_d2))
        elif user_input == 2:
            # Update specific time of the date
            print('Güncellemeyi yapacağınız gün \ The day you\'ll perform update:')
            date1 = regex_date()
            print('Güncellemek istediğiniz saat \ Time you want to update:')
            time1 = regex_time()
            print('Yeni saat değeri \ New time value:')
            time2 = regex_time()
            conn.execute('UPDATE veriler SET time = ? WHERE date = ? AND time = ?',
                         (time2, date1, time1))
        elif user_input == 3:
            # main menu
            return

        if user_input is 1 or 2 or 3:
            if user_input is 1 or 2:
                print('Veri güncelleme gerçekleşirildi. \ Recording is done')
            move_on = True
        else:
            print('Seçenekler arasında ' + str(user_input) + ' mevcut değil.'
                                                             '\nThere is not ' + str(user_input) + ' as an option')

        db.commit()


def dict_ts():
    # Creates dictionary and sorts array with time values
    dict_raw = {}
    dict_sort = {}
    for veri in conn.execute('SELECT date, time FROM veriler'):
        dict_raw.setdefault(veri[0], []).append(veri[1])
    for i, j in dict_raw.items():
        dict_sort.setdefault(i, sorted(j))

    return dict_sort


# Prints values as 00:00 > 00:00
def table_time_str(s1, s2):
    return str(s1 + ' > ' + s2)


# Calculates difference of the two time object
def difference(s1, s2):
    return dt.strptime(s2, timeFormat) - dt.strptime(s1, timeFormat)


# Prints table and then writes to txt file
def table_str(file, key, table_time, diff):
    info = '{0:12s} {1:15s} {2:7s}'.format(key, table_time, diff)
    print(info)
    file.write(info + '\n')


# Write to file
def txt_write(file, v_line):
    file.write(v_line)


# Write line to file
def txt_writelines(file, lines):
    file.writelines(lines)


# Calculate time difference between first and last time input
def calc_time():
    file_destination = folder_name + file_name + '.txt'
    file = open(file_destination, 'w')

    table_title = '{0:12s} {1:15s} {2:7s}'.format('Tarih', 'Saat', 'Süre')
    print(table_title)
    txt_write(file, table_title + '\n')

    # Store times to different arrays as before and after 17:30
    before_1730_list = []
    after_1730_list = []
    time_to_leave = '17:30'
    # Loops through time values
    for key, arr in dict_ts().items():
        min_value = min(arr)
        max_value = max(arr)
        if max_value <= time_to_leave:
            before_1730_list.append(str(difference(min_value, max_value)))
        else:
            before_1730_list.append(str(difference(min_value, time_to_leave)))
            after_1730_list.append(str(difference(time_to_leave, max_value)))
        table_str(file, str(key), table_time_str(min_value, max_value), str(difference(min_value, max_value)))

    # Create a time object to store total time
    total_1 = dt.strptime('01:00:00', timeFormat_with_day)
    total_2 = dt.strptime('00:00', timeFormat)
    for index in before_1730_list:
        # Split the time
        hrs, mins, secs = index.split(':')
        # Add one by one to total_1 time object if exceed 23:59 it increases the date
        total_1 = total_1 + datetime.timedelta(days=00, hours=int(hrs),
                                               minutes=int(mins))
    for index in after_1730_list:
        hrs, mins, secs = index.split(':')
        total_2 = total_2 + datetime.timedelta(hours=int(hrs),
                                               minutes=int(mins))
    # Total days from the database (get keys)
    number_of_days = 'Toplam gün \ Total days = ' + str(len(dict_ts().keys()))
    d, h, m = str(total_1.strftime(timeFormat_with_day)).split(':')
    shift = 'Toplam mesai \ Total shift= ' + str(int(d) - 1) + ' gün \ day + ' \
            + h + ':' + m + ' = ' + str((((int(d) - 1) * 24) + int(h))) + ':' + m
    extra_shift = 'Toplam fazla mesai (15:30 dan sonra) \ Total overtime = ' + total_2.strftime(timeFormat)
    print('\n' + number_of_days + '\n' + shift + '\n' + extra_shift)

    list_of_calc = ['\n', number_of_days + '\n', shift + '\n', extra_shift]
    txt_writelines(file, list_of_calc)
    file.close()


# Print raw data
def print_data():
    # for veri in conn.execute('SELECT date,time FROM veriler'):
    #     print(veri[0], veri[1])
    for i, j in dict_ts().items():
        print(i, j)  # sorted(j)


def choices():
    print('1 - Giriş kaydı \ Add now')
    print('2 - Veri ekle \ Add record')
    print('3 - Veri sil \ Delete record')
    print('4 - Veri Güncelle \ Update record')
    print('5 - Verileri yazdır \ Print records')
    print('6 - Süre hesapla \ Calculate time')
    print('7 - Çıkış \ Exit')


def exit_app():
    db.close()
    print('Veriler kayıt edildi. \ Records are saved.')
    print('Çıkmak için Enter a basın. \ Press Enter to exit.')
    input('')
    sys.exit()


def line():
    print('-------------------')


# All opreations
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
        update_date_time()
    elif user_input == 5:
        print_data()
    elif user_input == 6:
        calc_time()
    elif user_input == 7:
        exit_app()
    else:
        print('Seçenekler 1 den 7 ye kadar. Yapma gözünü seveyim.\n'
              'Please choose from 1 to 7.')
    print()
    line()
