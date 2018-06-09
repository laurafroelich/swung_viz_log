import unittest
import read_data
import lasio

class TestReading(unittest.TestCase):

    def test_reader(self):
        input_file = "../../EAGE2018/Well-A_finished/HQLD_B_2C1_75-1_Well-A_ISF-BHC-MSFL-GR__COMPOSIT__1.LAS"
        result = read_data.read(input_file)
        assert(isinstance(result, lasio.las.LASFile))