import sqlite3

def create_tables():
    database = sqlite3.connect('bot.db')
    cursor = database.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER NOT NULL UNIQUE,
        full_name TEXT NOT NULL,
        phone TEXT NOT NULL,
        password TEXT NOT NULL
        );
        ''')


    cursor.execute('''CREATE TABLE IF NOT EXISTS reviews (
        review_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        review_text TEXT NOT NULL
        );
        ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS translations (
        translation_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        original_text TEXT NOT NULL,
        translation_text TEXT NOT NULL
        );
        ''')

    database.commit()
    database.close()


create_tables()

#------------------------------------------------------------------------
# login

def get_user(telegram_id):
    database = sqlite3.connect('bot.db')
    cursor = database.cursor()

    cursor.execute('''SELECT * FROM users WHERE telegram_id = ?''', (telegram_id,))

    user = cursor.fetchone()

    database.close()

    return user

# register

def create_user(telegram_id, full_name, phone, password):
    database = sqlite3.connect('bot.db')
    cursor = database.cursor()

    cursor.execute('''
    INSERT INTO users (telegram_id, full_name, phone, password)
    VALUES (?, ?, ?, ?)
    ''', (telegram_id, full_name, phone, password))

    database.commit()
    database.close()



#------------------------------------------------------------------------
# review
def save_review(user_id, review_text):
    database = sqlite3.connect('bot.db')
    cursor = database.cursor()

    cursor.execute('''
         INSERT INTO reviews (user_id, review_text)
         VALUES (?, ?)''', (user_id, review_text))

    database.commit()
    database.close()



#------------------------------------------------------------------------
# translation

def save_translation(user_id, original_text, translation_text):
    database = sqlite3.connect('bot.db')
    cursor = database.cursor()

    cursor.execute('''
    INSERT INTO translations (user_id, original_text, translation_text)
    VALUES (?, ?, ?)''', (user_id, original_text, translation_text))

    database.commit()
    database.close()







