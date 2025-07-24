import os
import unittest
from datetime import datetime
from pathlib import Path

import pandas as pd

from toolkit.utils import misc
from toolkit.utils.get_variable_name import get_local_variable_name

# functions to test
from toolkit.utils.iohandler import IOHandler
from toolkit.utils.snake_case import snake_case


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

    def test_get_variable_name(self):
        a = 3

        def foo(x):
            return get_local_variable_name(x)

        assert foo(a) == "a"
        assert get_local_variable_name(a) is None

    def test_misc(self):
        input_dict = {"a": [1, 2], "b": ["A", "B"]}

        assert all(
            misc.expand_grid(input_dict)
            == pd.DataFrame(
                {
                    "a": [1, 1, 2, 2],
                    "b": [
                        "A",
                        "B",
                        "A",
                        "B",
                    ],
                }
            )
        )

        mystr = f"({round(1, 3):.{3}f}) - ["
        mystr += datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        mystr += "]"
        assert misc.step_time(step=1, digits=3)

    def test_snake_case(self):
        assert "aasdkjh213987-a-kh" == snake_case(string="aasdkjh213987_AKh")


if __name__ == "__main__":
    unittest.main()
