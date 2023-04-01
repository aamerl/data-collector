#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This contain the main function"""

__author__ = "Aamer Lhoussaine"
__copyright__ = "Copyright 2021, The Agric 4.0 project"
__email__ = "lhoussaine.aamer@outlook.fr"
__status__ = "Dev"

import time
import logging.config
from pymodbus.client.sync import ModbusSerialClient
from main.db.db import InfluxDB
from main.utils.utils import *


def main() -> None:
    # init args
    parser = init_argparse()
    args = parser.parse_args()
    # init logs
    logging.config.fileConfig('logging.ini')
    # read configuration file
    config, sensors, configuration_id, box_id = read_config_file(args.config)
    # rasp client
    rasp_client = ModbusSerialClient(method=config["rasp_client"]["method"],
                                     port=config["rasp_client"]["port"],
                                     timeout=config["rasp_client"]["timeout"],
                                     stopbits=config["rasp_client"]["stopbits"],
                                     bytesize=config["rasp_client"]["bytesize"],
                                     parity=config["rasp_client"]["parity"],
                                     baudrate=config["rasp_client"]["baudrate"])
    rasp_client.connect()
    # init influxdb client
    inf_client = InfluxDB(url=config["influxdb"]["url"],
                          token=config["influxdb"]["token"],
                          org=config["influxdb"]["org"]
                          )
    bucket = config["influxdb"]["bucket"]
    # init all sensors
    sensors = init_sensors(sensors, box_id, configuration_id)
    while True:
        # get data from sensors
        data = get_data(client=rasp_client, sensors=sensors)
        # send data to sqLite
        if data:
            inf_client.insert_measures(bucket=bucket, measures_list=data)
        # sleep time in the config file
        time.sleep(config["period"])


if __name__ == "__main__":
    main()
