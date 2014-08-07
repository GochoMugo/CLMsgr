import sqlite3
import unittest
from DM import api
from DM.utils import messages 


class API(unittest.TestCase):
    @unittest.skip('not syntatically correct yet...')
    def test_writing(self):
        'ensure the writing never raises an exception'
        assert api.write('test', 'testing')
        assert(api.write('test', 'testing', 0))
        assert(api.write('test', 'testing', 1))
        assert(api.write('test', 'testing', 2))


class Messages(unittest.TestCase):
    def setUp(self):
        self.db = '.test.db'

    def test_read(self):
        empty = messages.read('boom', self.db)
        msg = 'Msg DB Read did not return [] when table is missing'
        self.assertEqual(empty, [], msg)
        with sqlite3.connect(self.db) as db:
            cursor = db.cursor()
            sql = 'CREATE TABLE boom(bang)'
            # Ensure the table is created
            self.assertRaises(sqlite3.OperationalError, cursor.execute, sql)


if __name__ == '__main__':
    unittest.main()
