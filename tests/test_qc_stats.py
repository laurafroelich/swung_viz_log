import unittest
import calculate_qc_stats

class TestQCStats(unittest.TestCase):

    def test_count_folders(self):
        n_files = calculate_qc_stats.count_number_of_files('test_data/', 'txt')
        self.assertEquals(n_files, 5)