
# -*- coding: utf-8 -*-

__author__ = "Aamer Lhoussaine"
__email__ = "lhoussaine.aamer@outlook.fr"
__status__ = "Dev"

import unittest
from main.utils import read_config_file, init_sensors
from main.sensor.sensor import NPKSensor, THECSensor


class TestUtils(unittest.TestCase):

    def test_read_config_file(self):
        config, sensors, _, _ = read_config_file("tests/")
        self.assertEqual(1, config["configuration_id"])
        self.assertEqual(3, config["period"])
        self.assertEqual(2, len(sensors))
        self.assertEqual(1, sensors[0]["sensor_id"])
        self.assertEqual(2, sensors[1]["sensor_id"])

    def test_init_sensors(self):
        _, sensors, configuration_id, box_id = read_config_file("tests/")
        sensors_list = init_sensors(sensors, configuration_id, box_id)
        self.assertEqual(2, len(sensors))
        self.assertTrue(type(sensors_list[0] is NPKSensor))
        self.assertEqual(1, sensors_list[0].sensor_id)
        self.assertEqual("NPK", sensors_list[0].type)

        self.assertTrue(type(sensors_list[1] is THECSensor))
        self.assertEqual(2, sensors_list[1].sensor_id)
        self.assertEqual("THEC", sensors_list[1].type)

        self.assertEqual(configuration_id, 1)
        self.assertEqual(box_id, 1)


if __name__ == '__main__':
    unittest.main()
