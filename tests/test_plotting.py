import unittest
import read_data
import lasio
import plotting
import matplotlib.pyplot as plt

class TestPlotting(unittest.TestCase):

    def test_plot(self):
        input_file = "../../EAGE2018/Well-A_finished/HQLD_B_2C1_75-1_Well-A_ISF-BHC-MSFL-GR__COMPOSIT__1.LAS"
        result = read_data.read(input_file)

        result_keys = result.keys()

        plotting.plot_two_columns(result.df(), result_keys[1], result_keys[2])