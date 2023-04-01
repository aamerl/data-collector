#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains Sensor class that represent a physical sensor
"""
__author__ = "Aamer Lhoussaine"
__copyright__ = "Copyright 2021, The Agric 4.0 project"
__email__ = "lhoussaine.aamer@outlook.fr"
__status__ = "Dev"

from abc import ABC, abstractmethod
from typing import List
from pymodbus.client.sync import ModbusSerialClient
from main.sensor.measure import Measure


class Sensor(ABC):

    """[This class represent a sensor in a site, a sensor can contain one measure or multiple]

    Args:
        # undefined args are the arguments that are used by ModbusSerialClient
        sensor_id (int): the sensor id
        bytesize (int):
        timeout (int):
        method (str):
        stopbits (int):
        parity (int):
        port (str):
        baudrate (int):
        unit (int):
        count (int):
        type (str): the type of the sensor NPK, HMD ...
        measurement_list (list): a list of Measure objects
    """

    def __init__(self, sensor_id, bytesize, timeout, stopbits, parity, port, baudrate, unit,
                 count, type, method, measurement_list) -> None:
        self.sensor_id = sensor_id
        self.bytesize = bytesize
        self.timeout = timeout
        self.port = port
        self.sensor_id = sensor_id
        self.parity = parity
        self.stopbits = stopbits
        self.baudrate = baudrate
        self.unit = unit
        self.count = count
        self.type = type
        self.measurement_list = measurement_list
        self.method = method

    @abstractmethod
    def read_data(self, client, timestamp) -> List[Measure]:
        """[Read data from sensor and return the measurement with an utc timestamp]

        Returns:
            List[Measure]: [a list of Measure objects]

        """

    def init_client(self) -> ModbusSerialClient:
        """[init a new ModbusSerialClient client]

        Returns:
            ModbusSerialClient: [description]
        """

        client = ModbusSerialClient(method=self.method, port=self.port,
                                    timeout=self.timeout, stopbits=self.stopbits, bytesize=self.bytesize,
                                    parity=self.parity, baudrate=self.baudrate)
        return client

    @staticmethod
    def disconnect(client) -> bool:
        """[disconnect]

        Args:
            client ([type]): [description]

        Returns:
            bool: [description]
        """
        client.close()
