import sqlite3 as sq

# Проверка на бд
async def start():

    try:    
        db = sq.connect('shoes.db')
        cursor = db.cursor()
        
        print('Datebase connected')

    except sq.Error as e:
        print('ERROR',e)
    
    finally:
        cursor.close()
        db.commit()

#Читаем бд
async def read_sql():
    
    try:    
        db = sq.connect('shoes.db')
        cursor = db.cursor()
    
        data = cursor.execute('SELECT * FROM menu').fetchall()
    
        return data
    
    except sq.Error as e:
        print('ERROR',e)
    
    finally:
        cursor.close()
        db.commit()

async def add_product(state):

    try:    
        db = sq.connect('shoes.db')
        cursor = db.cursor()
        
        async with state.proxy() as data: 
            cursor.execute('INSERT INTO menu(photo, name, description, price, article) VALUES(?, ?, ?, ?, ?)', tuple(data.values()))

    except sq.Error as e:
        print('ERROR', e)
    
    finally:
        cursor.close()
        db.commit()

async def add_admin(admin):
    
    try:
        db = sq.connect('shoes.db')
        cursor = db.cursor()

        cursor.execute('INSERT INTO admin(id_admin) VALUES(?)', [admin])
        

    except SyntaxError as e:
        print('Error', e)

    finally:
        cursor.close()
        db.commit()


async def check_admin(id_):
    
    try:
        db = sq.connect('shoes.db')
        cursor = db.cursor()
        admin = cursor.execute('SELECT * FROM admin WHERE id_admin = ?', [id_]).fetchone()
        
        return admin
    
    except:
        print('Error')
    
    finally:
        cursor.close()
        db.commit()

async def delete_in_db(article):
    
    try:
        db = sq.connect('shoes.db')
        cursor = db.cursor()

        cursor.execute('DELETE FROM menu WHERE article = ?', [article])
    
    except SyntaxError as e:
        print('Error', e)
    
    finally:
        cursor.close()
        db.commit()