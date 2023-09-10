
# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Aamer Lhoussaine"
__email__ = "lhoussaine.aamer@outlook.fr"
__status__ = "Dev"

import unittest
from main.db.db import SQLDB


class TestSQLDB(unittest.TestCase):

    def test_connect(self):
        sqlDB1 = SQLDB("tests/db/test.db")
        self.assertTrue(sqlDB1.connect())

    def test_disconnect(self):
        sqlDB1 = SQLDB("tests/db/test.db")
        sqlDB1.connect()
        self.assertTrue(sqlDB1.disconnect())

    def test_insert_measures(self):
        measures_list = [(1, 1, 1, 1, 1630166458, 1.6),
                         (1, 2, 1, 1, 1630166458, 1.9),
                         (1, 3, 1, 1, 1630166458, 1.8),
                         (2, 1, 1, 1, 1630166458, 1.7)]

        sqlDB1 = SQLDB("tests/db/test.db")
        sqlDB1.connect()
        cur = sqlDB1.connection.cursor()
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS measures (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sensor_id INTEGER,
                    measure_id INTEGER,
                    configuration_id INTEGER,
                    box_id INTEGER,
                    timestamp INTEGER,
                    value REAL
                    );""")
        cond = sqlDB1.insert_measures(
            measures_list=measures_list, sql_table="measures",
            max_rows=10)

        self.assertTrue(cond)

        newMeasuresList = cur.execute(
            """SELECT sensor_id, measure_id, configuration_id, box_id, timestamp, value FROM measures""").fetchall()
        self.assertTrue((1, 1, 1, 1, 1630166458, 1.6) in newMeasuresList)
        self.assertTrue((1, 2, 1, 1, 1630166458, 1.9) in newMeasuresList)
        self.assertTrue((1, 3, 1, 1, 1630166458, 1.8) in newMeasuresList)
        self.assertTrue((2, 1, 1, 1, 1630166458, 1.7) in newMeasuresList)
        self.assertFalse((2, 1, 1, 1, 1630166458, 1.8) in newMeasuresList)


if __name__ == '__main__':
    unittest.main()
