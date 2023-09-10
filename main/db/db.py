#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module is for SQLite and InfluxDB Class
"""
__author__ = "Aamer Lhoussaine"
__email__ = "lhoussaine.aamer@outlook.fr"
__status__ = "Dev"

import sqlite3
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import logging
from typing import List


class SQLDB():
    """[All interaction with sqlite is done with this class]
    Args:
        path (str): the path where sqlite database is stored
    """

    def __init__(self, path) -> None:
        self.path = path
        self.connection = None

    def connect(self) -> bool:
        try:
            self.connection = sqlite3.connect(f"{self.path}")
            logging.info("success connection to sqlite")
            return True
        except Exception:
            logging.exception('error in connection to sqlite')
            return False

    def disconnect(self) -> bool:
        try:
            self.connection.close()
            logging.info("success disconnect from sqlite")
            return True
        except Exception:
            logging.exception(f'error to disconnect from sqlite')
            return False

    def insert_measures(self, measures_list: List, sql_table: str, max_rows) -> bool:
        try:
            cur = self.connection.cursor()
            x = cur.execute(f"""select count(*) from {sql_table}""").fetchone()[0]
            if x >= max_rows and x is not None:
                cur.execute(
                    f"""delete from {sql_table} where id IN (select id from {sql_table} order by id asc limit {len(measures_list)*4})""")
            cur.executemany(
                f"""
                insert into {sql_table}(sensor_id, measure_id, configuration_id, box_id, timestamp, value) values (?, ?, ?, ?, ?, ?);
                """,
                measures_list
            )
            self.connection.commit()
            logging.info("data inserted successfully in sqlite")
            return True

        except Exception:
            logging.exception(f'data are not inserted in sqlite')
            return False


class InfluxDB():
    """[All interaction with Influx database is done with this class]
    """

    def __init__(self, url, token, org) -> None:
        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def insert_measures(self, bucket: str, measures_list: List) -> bool:
        """_summary_

        Args:
            bucket (str): bucket where to store data in influxdb
            measures_list (List): a list of measurement (dict)

        Returns:
            bool: return if there is no exception when data is stored
        """
        try:
            self.write_api.write(bucket=bucket, record=measures_list, write_precision="s")
            logging.info('data inserted in influxdb')
            return True
        except Exception:
            logging.exception(f'data are not inserted in influxdb')
            return False
