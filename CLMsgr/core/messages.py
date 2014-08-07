'''
Messages utility. Handles saving and reading back messages.
The messages are stored in a sqlite3 database.
Each account has its own table. There's an extra table `recent`
that holds recently received messages.

Dependencies: __app_dir__, io
'''


import os
import sqlite3
import time
from . import __app_dir__
from . import io


home = os.path.expanduser('~')
msgs_db = os.path.join(__app_dir__, '.messages.db')


def read(account, db=msgs_db):
    msgs = []
    with sqlite3.connect(db) as db:
        cursor = db.cursor()
        try:
            sql = 'SELECT time, sender, content FROM "{0}"'.format(account)
            for msg in cursor.execute(sql).fetchall():
                msg = {
                    'time': msg[0],
                    'sender': msg[1],
                    'content': msg[2]
                }
                msgs.append(msg)
        except sqlite3.OperationalError:
            try:
                sql = 'CREATE TABLE "{0}"(time, sender, content)'.format(account)
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
    return msgs


def save(account, sender, content, db_file=msgs_db):
    with sqlite3.connect(db_file) as db:
        cursor = db.cursor()
        now = time.time()
        # rounding off is neccessary for read returns 2dp float no.s
        now = round(now, 2)
        try:
            sql = 'INSERT INTO "{0}" VALUES(?, ?, ?)'.format(account)
            cursor.execute(sql, (now, sender, content,))
            db.commit()
            recent(now, sender, content, db_file)
            return True
        except sqlite3.OperationalError:
            try:
                sql = 'CREATE TABLE "{0}"(time, sender, content)'.format(account)
                cursor.execute(sql)
                db.commit()
                sql = 'INSERT INTO "{0}" VALUES(?, ?, ?)'.format(account)
                cursor.execute(sql, (now, sender, content,))
                db.commit()
                recent(now, sender, content, db_file)
                return True
            except:
                db.rollback()
                return False
    return False


def delete_all(account, db=msgs_db):
    # Removing from Recent table
    accounts = read(account, db)
    if accounts:
        for acc in accounts:
            recent(acc['time'], acc['sender'], acc['content'],
                   db=db, aim='remove')
    # Removing everything from the messages table
    with sqlite3.connect(db) as db:
        cursor = db.cursor()
        try:
            sql = 'DELETE FROM "{0}"'.format(account)
            cursor.execute(sql)
            db.commit()
            return True
        except sqlite3.OperationalError:
            db.rollback()
            return False
    return False


def recent(now, sender, content, db=msgs_db, aim='add'):
    with sqlite3.connect(db) as db:
        cursor = db.cursor()

        def add():
            sql = 'INSERT INTO recent VALUES(?, ?, ?)'
            cursor.execute(sql, (now, sender, content,))

        def remove():
            sql = '''DELETE FROM recent
                       WHERE (time={0} AND sender="{1}"
                       AND  content="{2}")'''
            sql = sql.format(now, sender, content)
            cursor.execute(sql)

        if aim == 'add':
            aim = add
        elif aim == 'remove':
            aim = remove

        try:
            aim()
            db.commit()
            return True
        except sqlite3.OperationalError:
            try:
                sql = 'CREATE TABLE recent(time, sender, content)'
                cursor.execute(sql)
                db.commit()
                aim()
                db.commit()
                return True
            except:
                db.rollback()
                return False
    return False


def manage(aim, targets=None):
    ''' Handles messages stored by app.
    `aim` may be: `view`, `delete`
    '''
    # viewing accounts registered to channels
    if aim == 'view':
        if not targets:
            targets = ['recent']
        for target in targets:
            msgs = read(target)
            if msgs:
                if len(msgs) == 1:
                    confirmation = '1 message found'
                else:
                    confirmation = '{0} messages found'.format(len(msgs))
                io.write(target, confirmation)
                for msg in msgs:
                    row = '{hour}:{minute}.. {name}: {message}\n'.format(
                        hour=time.localtime(msg['time']).tm_hour,
                        minute=time.localtime(msg['time']).tm_min,
                        name=msg['sender'],
                        message=msg['content']
                    )
                    print(row)
            else:
                io.write(target, 'No messages found', 1)
    elif aim == 'delete':
        if not targets:
            io.write('', 'No channel specified', 1)
            return
        for target in targets:
            if delete_all(target):
                io.write(target, 'Messages deleted Successfully')
            else:
                io.write(target, 'Messages failed to be deleted', 1)
