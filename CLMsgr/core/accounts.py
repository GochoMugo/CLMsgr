'''
Handles getting/setting account configurations.

Dependencies: __app_dir__, io
'''


import os
import sqlite3
from . import __app_dir__
from . import io


# Default Accounts DB
accounts_db = os.path.join(__app_dir__, '.accounts.db')


def read(db=accounts_db):
    ''' Reads the accounts slightly*
    Returns a list of dict in the form: [{'type': 'username'}, ... ]
    '''
    content = []
    with sqlite3.connect(db) as db:
        cursor = db.cursor()
        try:
            sql = 'SELECT type, username FROM accounts'
            for item in cursor.execute(sql).fetchall():
                content.append({
                    'type': item[0],
                    'username': item[1]
                })
        except sqlite3.OperationalError:
            try:
                sql = 'CREATE TABLE accounts(type, username)'
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
    return content


def read_one(name, field, db=accounts_db):
    ''' Read a value set for an account.
    `name` - name of account e.g. twitter
    `field` - field/key to save with e.g. username
    Returns the value in the field specified.
    Returns None if not found'''

    with sqlite3.connect(db) as db:
        cursor = db.cursor()
        try:
            sql = 'SELECT {0} FROM accounts WHERE type=="{1}"'.format(field, name)
            result = cursor.execute(sql).fetchone()
            if result:
                return result[0]
            return None
        except sqlite3.OperationalError:
            try:
                sql = 'CREATE TABLE accounts(type, username, {0})'.format(field)
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
    return None


def save_one(name, field, value, db=accounts_db):
    '''Saves the value in the specified field.
    `name` - name of account e.g. twitter
    `field` - field/key to save with e.g. username
    `value` - value to save. e.g. stupid_username
    Returns True if successful, False if not.
    '''

    exists = read_one(name, field)
    with sqlite3.connect(db) as db:
        cursor = db.cursor()
        try:
            if not exists:
                try:
                    sql = 'ALTER TABLE accounts ADD {0}'.format(field)
                    cursor.execute(sql)
                    db.commit()
                except:
                    pass
            sql = 'UPDATE accounts SET {0}="{1}" WHERE type=="{2}"'
            sql = sql.format(field, value, name)
            cursor.execute(sql)
            db.commit()
            return True
        except sqlite3.OperationalError:
            db.rollback()
            return False
    return False


def search_username(name):
    '''' Searches for username set for a specific account.
    `name` - name of account e.g. twitter
    Returns the username. Else returns False.
    This is just a wrapper around read_one()'''

    username = read_one(name, 'username')
    if username:
        return username
    return False


def add_account(name, username, db=accounts_db):
    ''' Adds a new account.
    `name` - name of account e.g. twitter
    `username` - username to set for the new account. e.g. stupid_username
    If an account exists, it is overwritten.
    Returns True on success, False on failure.
    '''
    exists = search_username(name)
    with sqlite3.connect(db) as db:
        cursor = db.cursor()
        try:
            if exists:
                sql = 'UPDATE accounts SET username="{0}" WHERE type=="{1}"'
                sql = sql.format(username, name)
                cursor.execute(sql)
            else:
                sql = 'INSERT INTO accounts(type, username) VALUES (?,?)'
                cursor.execute(sql, (name, username,))
            db.commit()
            return True
        except sqlite3.OperationalError:
            db.rollback()
            return False
    return False


def remove_account(name, db=accounts_db):
    ''' Removes an account.
    `name` - name of the account e.g. twitter
    Returns True on success, False on failure.
    '''
    with sqlite3.connect(db) as db:
        cursor = db.cursor()
        try:
            sql = 'DELETE FROM accounts WHERE type == "{0}"'
            sql = sql.format(name)
            db.execute(sql)
            db.commit()
            return True
        except sqlite3.OperationalError:
            db.rollback()
            return False
    return False


def dummy_init(username=None):
    'Dummy/Stupid function that always return True'
    return True


def manage(aim, targets=[], username=None):
    '''Manages the accounts.
    `aim` may be 'add/remove/view'
    `targets` is an array with the names of the channels
    `username` is username used in the adding new accounts.
    '''
    # adding new channels
    if aim == 'add':
        for target in targets:
            if add_account(target, username):
                io.write(target, 'Account added')
                return True
            else:
                io.write(target, 'Account failed to be added', 1)
                return False
    # removing channels
    elif aim == 'remove':
        for target in targets:
            if remove_account(target):
                io.write(target, 'Account removed')
                return True
            else:
                io.write(target, 'Account failed to be removed', 1)
                return False
    # viewing accounts registered in channels
    elif aim == 'view':
        all_accounts = read()
        if all_accounts == []:
            io.write('', 'No Accounts found', 1)
        else:
            for account in all_accounts:
                io.write(account['type'], account['username'])
        return True
