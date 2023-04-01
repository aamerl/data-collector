#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains Measure Class that represent a physical measure that we obtain from sensors/raspberryPi
"""

__author__ = "Aamer Lhoussaine"
__copyright__ = "Copyright 2021, The Agric 4.0 project"
__email__ = "lhoussaine.aamer@outlook.fr"
__status__ = "Dev"

from dataclasses import dataclass


@dataclass
class Measure:
    """[This class represent one measure that we can retrieve from the sensor,
        Note: The sensor can have one or multiple measure]
    """

    measure_id: int
    sensor_id: int
    configuration_id: int
    box_id: int
    unit: str
    name: str
    address: str
    timestamp: int
    value: float
