import unittest
from package.module import parse_bin, Command, Parser, handle_line, Symbol, generate_binary_code


class TestCommandMethods(unittest.TestCase):

    def test_parse_bin(self):
        self.assertEqual(parse_bin(0), '0000000000000000')
        self.assertEqual(parse_bin(1), '0000000000000001')
        self.assertEqual(parse_bin(10), '0000000000001010')

    def test_l_command(self):
        l = Command('(LOOP)')
        self.assertEqual(l.type, 'L_COMMAND')
        self.assertEqual(l.symbol, 'LOOP')
        self.assertEqual(l.bincode, '')

    def test_a_command(self):
        a = Command('@1')
        self.assertEqual(a.type, 'A_COMMAND')
        self.assertEqual(a.symbol, '')
        self.assertEqual(a.bincode, '0000000000000001')

        a = Command('@LOOP')
        self.assertEqual(a.type, 'A_COMMAND')
        self.assertEqual(a.symbol, 'LOOP')
        self.assertEqual(a.bincode, '')

        a = Command('@i')
        self.assertEqual(a.type, 'A_COMMAND')
        self.assertEqual(a.symbol, 'i')
        self.assertEqual(a.bincode, '')

        a = Command('@R0')
        self.assertEqual(a.type, 'A_COMMAND')
        self.assertEqual(a.symbol, 'R0')
        self.assertEqual(a.bincode, '')

        a = Command('@ponggame.run')
        self.assertEqual(a.type, 'A_COMMAND')
        self.assertEqual(a.symbol, 'ponggame.run')
        self.assertEqual(a.bincode, '')

    def test_c_command(self):
        c = Command('D=A')
        self.assertEqual(c.type, 'C_COMMAND')
        self.assertEqual(c.dest, 'D')
        self.assertEqual(c.comp, 'A')
        self.assertEqual(c.jump, '')

        c = Command('AMD=D&A')
        self.assertEqual(c.type, 'C_COMMAND')
        self.assertEqual(c.dest, 'AMD')
        self.assertEqual(c.comp, 'D&A')
        self.assertEqual(c.jump, '')

        c = Command('0;JGE')
        self.assertEqual(c.type, 'C_COMMAND')
        self.assertEqual(c.dest, '')
        self.assertEqual(c.comp, '0')
        self.assertEqual(c.jump, 'JGE')


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

        data = '   D=M              // D = first number'
        line = handle_line(data)
        self.assertEqual(line, 'D=M')

        data = '   @R0'
        line = handle_line(data)
        self.assertEqual(line, '@R0')

        data = ''
        line = handle_line(data)
        self.assertEqual(line, None)

        data = '(OUTPUT_FIRST)'
        line = handle_line(data)
        self.assertEqual(line, '(OUTPUT_FIRST)')

    def test_construct_parser(self):
        add_path = '../projects/06/add/Add.asm'
        hack_path = '../projects/06/add/Add.hack'
        asm = Parser('add')
        self.assertEqual(asm.path, add_path)
        self.assertEqual(asm.hack_path, hack_path)

    def test_readfile_parser(self):
        fname = 'add'
        asm = Parser(fname)
        self.assertEqual(asm.lines, ['@2', 'D=A', '@3', 'D=D+A', '@0', 'M=D'])

        fname = 'max'
        asm = Parser(fname)
        self.assertEqual(asm.lines, ['@R0', 'D=M', '@R1', 'D=D-M', '@OUTPUT_FIRST', 'D;JGT', '@R1', 'D=M', '@OUTPUT_D',
                                     '0;JMP', '(OUTPUT_FIRST)', '@R0', 'D=M', '(OUTPUT_D)', '@R2', 'M=D', '(INFINITE_LOOP)', '@INFINITE_LOOP', '0;JMP'])


class TestSymbolMethod(unittest.TestCase):

    def test_symbol_method(self):
        # Constructor
        s = Symbol()
        self.assertEqual(len(s.table), 23)
        self.assertEqual(len(s.comp), 28)
        self.assertEqual(len(s.dest), 8)
        self.assertEqual(len(s.jump), 8)

        self.assertEqual(s.getAddress('R0'), 0)
        self.assertEqual(s.getAddress('SP'), 0)

        self.assertTrue(s.contains('R0'))
        self.assertTrue(s.contains('SP'))
        self.assertFalse(s.contains('R16'))

        self.assertFalse(s.contains('FOO'))
        s.addEntry('FOO', 16)
        self.assertEqual(s.getAddress('FOO'), 16)

    def test_convert_binary(self):
        s = Symbol()
        comp = '0'
        dest = 'M'
        jump = 'JGT'
        self.assertEqual(s.comp[comp], '0101010')
        self.assertEqual(s.dest[dest], '001')
        self.assertEqual(s.jump[jump], '001')

        dest = ''
        jump = ''
        self.assertEqual(s.dest[dest], '000')
        self.assertEqual(s.jump[jump], '000')

    def test_incre_current_addr(self):
        s = Symbol()
        self.assertEqual(s.current_addr, 16)
        s.incre_current_addr()
        s.incre_current_addr()
        self.assertEqual(s.current_addr, 18)

    def test_incre_running_num(self):
        s = Symbol()
        self.assertEqual(s.running_num, 0)
        s.incre_running_num()
        s.incre_running_num()
        self.assertEqual(s.running_num, 2)

class TestHandleBinaryCode(unittest.TestCase):
    def test_generate_binary_code(self):
        s = Symbol()
        # l = Command('(LOOP)')

        a = Command('@1')
        code = generate_binary_code(a, s)
        self.assertEqual(code, '0000000000000001')

        c = Command('D=A')
        code = generate_binary_code(c, s)
        self.assertEqual(code, '1110110000010000')

        c = Command('MD=D+1')
        code = generate_binary_code(c, s)
        self.assertEqual(code, '1110011111011000')


if __name__ == '__main__':
    unittest.main()
