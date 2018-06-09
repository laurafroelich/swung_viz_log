import unittest
import calculate_qc_stats

class TestQCStats(unittest.TestCase):

    def test_count_files_of_type(self):
        n_files = calculate_qc_stats.count_number_of_particular_files('test_data/', 'txt')
        self.assertEquals(n_files, 5)

    def test_count_files(self):
        n_files = calculate_qc_stats.count_number_of_files('test_data/')
        self.assertEquals(n_files, 6)