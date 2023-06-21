import serial

def test_serial_1():
    assert serial.find_series(name_file = "pytest",  type_file = "csv") == None