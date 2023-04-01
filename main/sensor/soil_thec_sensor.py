#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Class for THEC sensor
The S-Soil MT-02 soil moisture & temperature sensor is provided with high accurate and high sensitive.
By measuring the dielectric constant of the reaction of soil, soil direct stable real moisture content
"""

__author__ = "Aamer Lhoussaine"
__copyright__ = "Copyright 2021, The Agric 4.0 project"
__email__ = "lhoussaine.aamer@outlook.fr"
__status__ = "Dev"

from typing import List
from main.conf.constants import THEC_VWC, THEC_TEMP
from main.sensor.sensor import Sensor
from main.sensor.measure import Measure


class THECSensor(Sensor):
    """[summary]

    Args:
        Sensor ([type]): [description]
    """

    def read_data(self, client, timestamp) -> List[Measure]:
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
