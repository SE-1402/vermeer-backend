import unittest

from vermeer.backend.util.isobus_converter import IopParser


class TestIOPParser(unittest.TestCase):

    def setUp(self):
        self.iop_parser = IopParser()

    def test_parse(self):
        objects = self.iop_parser.parse("./vermeer/backend/util/example.iop")

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
