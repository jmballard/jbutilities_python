import os
import unittest
from pathlib import Path

# functions to test
from toolkit.utils.iohandler import IOHandler


class TestUtils(unittest.TestCase):

    def test_handler(self):
        io_expected = {
            "test1": 1,
            "test2": 2,
            "test_file_path": os.path.join(Path(__file__).parent, "test_file.txt"),
            "test_dir": os.path.join(Path(__file__).parent),
        }

        io_actual = IOHandler(io_expected)

        # test that the init went well
        assert io_expected["test1"] == io_actual["test1"]
        assert io_expected["test2"] == io_actual["test2"]
        assert io_expected["test_file_path"] == io_actual["test_file_path"]
        assert io_expected["test_dir"] == io_actual["test_dir"]

        # test listing files
        # print(io_actual.list_files('test_dir'))
        assert io_actual.list_files("test_dir") == [
            "test_data.py",
            "test_model_glm.py",
            "test_utils.py",
            "__init__.py",
            "__pycache__",
        ]

        # test the serial methods
        assert io_actual.find_last_version("test_file_path") is None
        assert io_actual.next_version("test_file_path") == io_expected["test_file_path"]


if __name__ == "__main__":
    unittest.main()
