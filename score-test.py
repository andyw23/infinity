import unittest

from importer import *


class SamplesTest(unittest.TestCase):
    def test_samples_have_variants(self):
        num = samples.Sample.num_samples_without_variants()
        self.assertTrue(num==0, "{0} Samples found without variants".format(num))


class ScoresTest(unittest.TestCase):

if __name__ == '__main__':
    unittest.main()
