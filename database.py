import sqlite3
import tkinter as tk
import keyboard

# Создание соединения с базой данных и таблицами
conn = sqlite3.connect('test.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS Good (name TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS Bad (name TEXT, count INTEGER DEFAULT 0)')

# Функция добавления выделенного текста в таблицу Good
def add_to_good():
    name = root.clipboard_get()
    c.execute('INSERT INTO Good (name) VALUES (?)', (name,))
    conn.commit()
    print(f'Name {name} added to Good')
    update_display(name)

# Функция добавления выделенного текста в таблицу Bad
def add_to_bad():
    name = root.clipboard_get()
    # Проверка, есть ли имя в таблице Bad
    c.execute('SELECT * FROM Bad WHERE name = ?', (name,))
    row = c.fetchone()
    if row is not None:
        # Если имя уже есть в таблице, увеличить счетчик на 1
        count = row[1] + 1
        c.execute('UPDATE Bad SET count = ? WHERE name = ?', (count, name))
        conn.commit()
        if count >= 10:
            print(f'Name {name} added to Bad, count: {count}')
        else:
            print(f'Name {name} added to Bad, count: {count}')
    else:
        # Если имя не найдено в таблице, добавить его со счетчиком 1
        c.execute('INSERT INTO Bad (name) VALUES (?)', (name,))
        conn.commit()
        print(f'Name {name} added to Bad, count: 1')
    update_display(name)

# Функция обновления информации в графическом интерфейсе
def update_display(name):
    # Получение количества имени в таблицах Bad и Good
    c.execute('SELECT COUNT(*) FROM Bad WHERE name = ?', (name,))
    bad_count = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM Good WHERE name = ?', (name,))
    good_count = c.fetchone()[0]

    # Обновление отображаемой информации в виджетах
    bad_name_label.config(text=f'Bad: {bad_count}')
    good_name_label.config(text=f'Good: {good_count}')
    name_label.config(text=f'{name}')

root = tk.Tk()

name_label = tk.Label(root, text='Name', font=('Arial', 24))
name_label.pack()

good_name_label = tk.Label(root, text='Good: 0', font=('Arial', 18))
good_name_label.pack()

bad_name_label = tk.Label(root, text='Bad: 0', font=('Arial', 18))
bad_name_label.pack()

###Добавить кнопки ?????????



root.mainloop()


# Закрытие соединения с базой данных
conn.close()
