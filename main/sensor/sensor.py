#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains Sensor class that represent a physical sensor
"""
__author__ = "Aamer Lhoussaine"
__email__ = "lhoussaine.aamer@outlook.fr"
__status__ = "Dev"

from typing import List
from abc import ABC, abstractmethod
from typing import List
from pymodbus.client.sync import ModbusSerialClient
from main.sensor.measure import Measure
from main.constants import THEC_VWC, THEC_TEMP


class Sensor(ABC):

    """[This class represent a sensor in a site, a sensor can contain one measure or multiple]

    Args:
        # undefined args are the arguments that are used by ModbusSerialClient ==> check pymodbus lib docs
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

    def __init__(self, sensor_id: int, bytesize: int, timeout: int, stopbits: int, parity: int, port: str, baudrate: int, unit: int,
                 count: int, type: str, method, measurement_list: List[Measure]) -> None:
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

    def __repr__(self) -> str:
        return f"sensor {self.sensor_id} type : {self.type}"

    @abstractmethod
    def read_data(self, client: ModbusSerialClient, timestamp: int) -> List[Measure]:
        """[Read data from sensor and return the measurement with an utc timestamp]

        Args:
            client (ModbusSerialClient): the client to read data
            timestamp (int): the timestamp to assign with data read from the sensor using <client>

        Returns:
            List[Measure]: [a list of Measure objects]

        """

    def init_client(self) -> ModbusSerialClient:
        """[init a new ModbusSerialClient client and return it]

        Returns:
            ModbusSerialClient
        """

        client = ModbusSerialClient(method=self.method, port=self.port,
                                    timeout=self.timeout, stopbits=self.stopbits, bytesize=self.bytesize,
                                    parity=self.parity, baudrate=self.baudrate)
        return client

    @staticmethod
    def disconnect(client) -> None:
        """[disconnect ModbusSerialClient]

        Args:
            client ModbusSerialClient: client to disconnect
        """
        client.close()


class NPKSensor(Sensor):
    """[Class represent a sensor of type NPK]

    Args:
        Sensor (ModbusSerialClient): client to use to read NPK data
    """

    def read_data(self, client, timestamp) -> List[Measure]:
        """
        For Docs check Sensor Parent class docs
        """
        if client is None:
            client = self.init_client()

        results = []

        for measure in self.measurement_list:
            measure.timestamp = timestamp
            measure.value = client.read_input_registers(address=int(measure.address, 16),
                                                        count=self.count, unit=self.unit)
            measure.value = measure.value.registers[0]
            results.append(measure)

        return results


class THECSensor(Sensor):
    """[Class represent a sensor of type THEC]

    Args:
        Sensor (ModbusSerialClient): client to use to read NPK data
    """

    def read_data(self, client, timestamp) -> List[Measure]:
        """
        For Docs check Sensor Parent class docs
        """
        results = []
        if client is None:
            client = self.init_client()

        for measure in self.measurement_list:
            measure.timestamp = timestamp
            value = client.read_input_registers(address=int(measure.address, 16),
                                                count=self.count, unit=self.unit)
            value = value.registers[0]

            if measure.address == THEC_TEMP:
                measure.value = float(value)/100
            elif measure.address == THEC_VWC:
                measure.value = float(value)/10000
            else:
                measure.value = float(value)

            results.append(measure)

        return results
