#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class for NPK sensor
The soil nitrogen, phosphorus and potassium sensor is suitable for detecting the content
of nitrogen, phosphorus and potassium in the soil
"""
__author__ = "Aamer Lhoussaine"
__copyright__ = "Copyright 2021, The Agric 4.0 project"
__email__ = "lhoussaine.aamer@outlook.fr"
__status__ = "Dev"

from typing import List
from main.sensor.sensor import Sensor
from main.sensor.measure import Measure


class NPKSensor(Sensor):
    """[summary]

    Args:
        Sensor ([type]): [description]
    """

    def read_data(self, client, timestamp) -> List[Measure]:
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
