import unittest

import numpy as np
import pandas as pd

# functions to test
from toolkit.models import glm


class TestGLMMethods(unittest.TestCase):

    def test_utils_correct_pred(self):
        expected = pd.Series(
            [
                0.024712048156881883,
                0.0316523470606187,
                0.023279259388849338,
                0.01621809888432968,
                0.03285105092243923,
                0.03285084181523246,
                0.015826084947343055,
                0.02219338101204149,
                0.03599369222820725,
                0.024269154696098694,
            ]
        )

        np.random.seed(42)
        preds = pd.Series(np.random.normal(loc=0.5, scale=0.1, size=10))

        actual = glm.utils.correct_pred(
            predictions=preds, original_avg=0.5, new_avg=0.03
        )

        assert all(actual == expected)


if __name__ == "__main__":
    unittest.main()
