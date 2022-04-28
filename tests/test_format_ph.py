from unittest import TestCase
import h2p_parser.format_ph as ph


class TestFormatPh(TestCase):

    def setUp(self):
        self.data_sds = [
            "HH AE1 M AA2 R K",
            "P ER0 S EH1 N T",
            "AO1",
            "P AA1 R K",
            "K AA1 N S OW0 L"
        ]
        self.data_list = [
            ['HH', 'AE1', 'M', 'AA2', 'R', 'K'],
            ['P', 'ER0', 'S', 'EH1', 'N', 'T'],
            ['AO1'],
            ['P', 'AA1', 'R', 'K'],
            ['K', 'AA1', 'N', 'S', 'OW0', 'L']
        ]

    # noinspection PyTypeChecker
    def test_to_sds(self):
        # Test str input
        for sds in self.data_sds:
            self.assertEqual(ph.to_sds(sds), sds)

        # Test for list input
        for ls, sds in zip(self.data_list, self.data_sds):
            self.assertEqual(ph.to_sds(ls), sds)

        # Test for nested list input
        for ls, sds in zip(self.data_list, self.data_sds):
            self.assertEqual(ph.to_sds([ls]), sds)

        # Test type errors
        with self.assertRaises(TypeError):
            ph.to_sds(1)
        with self.assertRaises(TypeError):
            ph.to_sds([1])
        with self.assertRaises(TypeError):
            ph.to_sds([[5], [1]])

        # Test for None in list
        self.assertEqual(ph.to_sds([None]), None)
        self.assertEqual(ph.to_sds([[None]]), None)

        # Test for empty list
        self.assertEqual(ph.to_sds([]), None)
        self.assertEqual(ph.to_sds([[]]), None)

    # noinspection PyTypeChecker
    def test_to_list(self):
        # Test standard input
        for ls, sds in zip(self.data_list, self.data_sds):
            self.assertEqual(ph.to_list(sds), ls)  # str input
            self.assertEqual(ph.to_list(ls), ls)  # list input
            self.assertEqual(ph.to_list([ls]), ls)  # nested list input

        # Test for none in list
        self.assertEqual(ph.to_list(None), None)

        # Test for empty list
        self.assertEqual(ph.to_list([]), None)
        self.assertEqual(ph.to_list([[]]), None)

        # Test for None in list
        self.assertEqual(ph.to_list([None]), None)
        self.assertEqual(ph.to_list([[None]]), None)

        # Test for empty list
        self.assertEqual(ph.to_list([]), None)
        self.assertEqual(ph.to_list([[]]), None)

        # Test type errors
        with self.assertRaises(TypeError):
            ph.to_list(1)
        with self.assertRaises(TypeError):
            ph.to_list([1])
        with self.assertRaises(TypeError):
            ph.to_list([[5], [1]])

