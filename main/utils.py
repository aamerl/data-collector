#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module for all function that can help in the process
Each function will be described
"""
__author__ = "Aamer Lhoussaine"
__email__ = "lhoussaine.aamer@outlook.fr"
__status__ = "Dev"

import argparse
import logging
import json
import time
from typing import List
from main.sensor.sensor import Sensor, THECSensor, NPKSensor
from pymodbus.client.sync import ModbusSerialClient
from main.sensor.measure import Measure
from main import constants


def init_argparse() -> argparse.ArgumentParser:
    """[init arge parse for the main]

    Returns:
        argparse.ArgumentParser: [arguments parser for the main.py]
    """
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [PATH]...",
        description="Collect data from sensors/Raspberrypi and send it to sqLite."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{parser.prog} version 1.0.0"
    )
    parser.add_argument('-c', '--config', help="path to the config.json file", required=True)
    parser.add_argument('-d', '--dbpath', help="path to the sqlite database file", required=False)

    return parser


def read_config_file(path: str):
    """[read json config file]

    Args:
        path (str): [path the json config file]

    Returns:
        [type]: [return a json config with a list of sensors]
    """
    try:
        with open(f'{path}/config.json') as file:
            config = json.load(file)
            sensors = list(config["sensors"])
            configuration_id = config["configuration_id"]
            box_id = config["box_id"]
        logging.info("success reading of config json file")

    except Exception:
        logging.exception('read config file')
        return False

    return config, sensors, configuration_id, box_id


def init_sensors(sensors: List, box_id: int, configuration_id: int) -> List:
    """[summary]

    Args:
        sensors (List): [a list of configs for each sensor]

    Returns:
        List: [list of Sensor objects]
    """
    sensors_list = []
    for sensor in sensors:
        # if the sensor is configured to not be used skip to next sensor
        if not sensor["active"]:
            continue

        measure_list = []
        for measure in sensor["measures"]:
            measure_list.append(Measure(
                measure_id=measure["measure_id"],
                sensor_id=sensor["sensor_id"],
                unit=sensor["unit"],
                name=measure["name"],
                address=measure["address"],
                configuration_id=configuration_id,
                box_id=box_id,
                timestamp=0,
                value=0
            ))

        if sensor["type"] == constants.NPK:
            sensors_list.append(NPKSensor(sensor_id=sensor["sensor_id"],
                                          bytesize=sensor["bytesize"],
                                          timeout=sensor["timeout"],
                                          stopbits=sensor["stopbits"],
                                          parity=sensor["parity"],
                                          port=sensor["port"],
                                          baudrate=sensor["baudrate"],
                                          unit=sensor["unit"],
                                          count=sensor["count"],
                                          type=sensor["type"],
                                          method=sensor["method"],
                                          measurement_list=measure_list))

        if sensor["type"] == constants.THEC:
            sensors_list.append(THECSensor(sensor_id=sensor["sensor_id"],
                                           bytesize=sensor["bytesize"],
                                           timeout=sensor["timeout"],
                                           stopbits=sensor["stopbits"],
                                           parity=sensor["parity"],
                                           port=sensor["port"],
                                           baudrate=sensor["baudrate"],
                                           unit=sensor["unit"],
                                           count=sensor["count"],
                                           type=sensor["type"],
                                           method=sensor["method"],
                                           measurement_list=measure_list))
    return sensors_list


def get_data(client: ModbusSerialClient, sensors: List[Sensor]) -> List:
    """[get data from all sensors and return a list of measure]

    Args:
        client (ModbusSerialClient): [description]
        sensors (List[Sensor]): [description]

    Returns:
        List: [description]
    """
    timestamp = int(time.time())
    data = []
    for sensor in sensors:
        try:
            sensor_measures = sensor.read_data(client=client, timestamp=timestamp)
            data.extend(sensor_measures)
        except Exception:
            logging.warning(f"read data error for sensor_id: {sensor.sensor_id}")
            try:
                client_temp = ModbusSerialClient(method=sensor.method,
                                                 port=sensor.port,
                                                 timeout=sensor.timeout,
                                                 stopbits=sensor.stopbits,
                                                 bytesize=sensor.bytesize,
                                                 parity=sensor.parity,
                                                 baudrate=sensor.baudrate)
                client_temp.connect()
                sensor_measures = sensor.read_data(client=client_temp, timestamp=timestamp)
                data.extend(sensor_measures)
                client_temp.close()
            except Exception:
                logging.warning(f"check configuration for this sensor_id: {sensor.sensor_id}")

    data_db = []
    if data:
        for measure in data:
            # sensor_id, measure_id, timestamp, value
            data_db.append({
                "measurement": "measure",
                "tags": {
                    "sensor_id": measure.sensor_id,
                    "measure_id": measure.measure_id,
                    "configuration_id": measure.configuration_id,
                    "box_id": measure.box_id
                },
                "fields": {
                    "value": float(measure.value)
                },
                "time": timestamp
            })

    return data_db
