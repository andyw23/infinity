import unittest

from importer import samples, components, choices, concerts, scores

samples.load_components()
choices.load_components()
concerts.load_components()
scores.load_components()


class ComponentsTest(unittest.TestCase):
    def test_event_loading_for_all_base_components(self):
        # chs = components.Component.get_by_type('CHOICE')
        # for ch in chs:
        #     ch.test_get_all_option_events()
        cts = components.Component.get_by_type('CONCERT')
        for ct in cts:
            ct.get_sample_components(0.0, None)

class SamplesTest(unittest.TestCase):
    def test_samples_have_variants(self):
        num = samples.Sample.num_samples_without_variants()
        self.assertTrue(num == 0, "{0} Samples found without variants".format(num))


if __name__ == '__main__':
    unittest.main()
