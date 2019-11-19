import unittest
from package.module import handle_line


class TestParserMethod(unittest.TestCase):
    def test_handle_line(self):
        data = '// This file is part of www.nand2tetris.org'
        line = handle_line(data)
        self.assertEqual(line, None)

        data = '\r\n'
        line = handle_line(data)
        self.assertEqual(line, None)

        data = '\n'
        line = handle_line(data)
        self.assertEqual(line, None)

        data = 'push constant 7'
        line = handle_line(data)
        self.assertEqual(line, ['push', 'constant', '7'])

        data = 'add'
        line = handle_line(data)
        self.assertEqual(line, ['add'])


if __name__ == '__main__':
    unittest.main()
