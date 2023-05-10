import sqlite3 as sq

async def start():

    try:    
        db = sq.connect('user.db')
        cursor = db.cursor()
        
        print('Datebase_user connected')

    except sq.Error as e:
        print('ERROR',e)
    
    finally:
        cursor.close()
        db.commit()

async def new_user(id_user):

    try:
        db = sq.connect('user.db')
        cursor = db.cursor()
        cursor.execute('INSERT INTO user(id_user) VALUES(?)',[id_user])

    except sq.Error as e:
        print('ERROR',e)
    
    finally:
        cursor.close()
        db.commit()

async def registor(state, user_id):
    try:
        db = sq.connect('user.db')
        cursor = db.cursor()
        
        async with state.proxy() as date:
            
            date = list(date.values())
            date.append(user_id)
            
            cursor.execute('UPDATE user SET name = ?, address = ?, phone = ? WHERE id_user = ?', date)

    except sq.Error as e:
        print('ERROR', e)
    
    finally:
        cursor.close()
        db.commit()

async def check_user(id_user):
        
    try:
        db = sq.connect('user.db')
        cursor = db.cursor()
        user = cursor.execute('SELECT * FROM user WHERE id_user = ?', [id_user]).fetchone()
        
        return user
    
    except:
        print('Error')
    
    finally:
        cursor.close()
        db.commit()

async def check_all_user():
    
    try:
        db = sq.connect('user.db')
        cursor = db.cursor()
        user = cursor.execute('SELECT * FROM user').fetchall()
        
        return user
    
    except:
        print('Error')
    
    finally:
        cursor.close()
        db.commit()