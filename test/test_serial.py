import unittest

import toolkit.serial as serial


class TestSerial(unittest.TestCase):
    def test_serial_1(self):
        assert serial.find_series(name_file="pytest", type_file="csv") is None


if __name__ == "__main__":
    unittest.main()
