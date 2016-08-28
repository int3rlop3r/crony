import os
import unittest
from crony import parsers

BASEPATH = os.path.dirname(os.path.abspath(__file__)) + '/'

class TestParsers(unittest.TestCase):

    def test_parse_range(self):
        # test normal comma separated range
        range_str1 = '1,2,3,4,5'
        range_set1 = set([1, 2, 3, 4, 5])
        self.assertEquals(parsers.parse_range(range_str1), range_set1)

        # test range with hyphen
        range_str2 = '1-5,9-13'
        range_set2 = set([1, 2, 3, 4, 5, 9, 10, 11, 12, 13])
        self.assertEquals(parsers.parse_range(range_str2), range_set2)

        # test adding an invalid job
        with self.assertRaises(ValueError):
            # 0 is an invalid id
            parsers.parse_range('0-5,9-13')

    def test_parse_file(self):
        # parse using filepath
        jobs1 = parsers.parse_file(cronfile=BASEPATH + 'cronfile')
        self.assertEquals(len(jobs1), 3)

        # parse using file descriptor
        parsers.parse_file(cronfd=open(BASEPATH + 'cronfile'))
        self.assertEquals(len(jobs1), 3)

