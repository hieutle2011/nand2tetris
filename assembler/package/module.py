import re


class Parser:
    def __init__(self, fname):
        # table mapping file name and file path
        self.map = {'add': '../projects/06/add/Add.asm',
                    'max': '../projects/06/max/Max.asm',
                    'maxl': '../projects/06/max/MaxL.asm',
                    'pongl': '../projects/06/pong/PongL.asm',
                    'pong': '../projects/06/pong/Pong.asm',
                    'rect': '../projects/06/rect/Rect.asm',
                    'rectl': '../projects/06/rect/RectL.asm'}
        if fname in self.map:
            self.path = self.map[fname]
            self.hack_path = self.map[fname].replace('asm', 'hack')
        else:
            self.path = ''
        self.lines = []

        # check file name
        if self.path == '':
            print('Wrong file name.')
            print('Valid names: add, max, maxl, pong, pongl, rect, rectl')
            exit()

        # initilize lines
        f = open(self.path, 'r')
        for line in f:
            new_line = handle_line(line)
            if new_line is not None:
                self.lines.append(new_line)
        f.close()


class Command:

    def __init__(self, code):
        self.code = code
        self.type = ''
        self.symbol = ''
        self.dest = ''
        self.comp = ''
        self.jump = ''
        self.bincode = ''
        self.regex = r"((?P<dest>[A-Z]*)=)*(?P<comp>[^;=\s]*)(;(?P<jump>[JELMNQTPTG]*))*"

        if self.code.startswith('('):
            self.type = 'L_COMMAND'
            value = self.code[1:-1]
            self.symbol = value
        elif self.code.startswith('@'):
            self.type = 'A_COMMAND'
            value = self.code[1:]
            if value.isdigit():
                self.bincode = parse_bin(int(value))
            else:
                self.symbol = value
        else:
            self.type = 'C_COMMAND'
            m = re.search(self.regex, self.code)
            dest = m.group('dest')
            comp = m.group('comp')
            jump = m.group('jump')
            if dest is not None:
                self.dest = dest
            if comp is not None:
                self.comp = comp
            if jump is not None:
                self.jump = jump


class Symbol:
    def __init__(self):
        # Each variable is assigned a unique memory address, starting at 16
        self.current_addr = 16

        self.running_num = 0

        # Pre-defined symbols: represent special memory locations
        self.table = {'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4, 'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6,
                      'R7': 7, 'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15, 'SCREEN': 16384, 'KBD': 24576}

        # Translating C-instruction
        self.comp = {'0': '0101010', '1': '0111111', '-1': '0111010', 'D': '0001100', 'A': '0110000', '!D': '0001101', '!A': '0110001', '-D': '0001111', '-A': '0110011', 'D+1': '0011111', 'A+1': '0110111', 'D-1': '0001110', 'A-1': '0110010', 'D+A': '0000010',
                     'D-A': '0010011', 'A-D': '0000111', 'D&A': '0000000', 'D|A': '0010101', 'M': '1110000', '!M': '1110001', '-M': '1110011', 'M+1': '1110111', 'M-1': '1110010', 'D+M': '1000010', 'D-M': '1010011', 'M-D': '1000111', 'D&M': '1000000', 'D|M': '1010101'}
        self.dest = {'': '000', 'M': '001', 'D': '010', 'MD': '011',
                     'A': '100', 'AM': '101', 'AD': '110', 'AMD': '111'}
        self.jump = {'': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011',
                     'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'}

    def addEntry(self, symbol, address):
        self.table[symbol] = address

    def getAddress(self, symbol):
        return self.table[symbol]

    def contains(self, symbol):
        return symbol in self.table

    def incre_current_addr(self):
        self.current_addr += 1

    def incre_running_num(self):
        self.running_num += 1


def parse_bin(num):
    prefix = ''
    binvalue = bin(num)[2:]
    for _ in range(16 - len(binvalue)):
        prefix += '0'
    return prefix + binvalue


def handle_line(line):
    if line.startswith('//') or line in ['\n', '\r\n', '']:
        return None
    else:
        return line.lstrip().split()[0]


def generate_binary_code(command, symbol):
    if command.type == 'L_COMMAND':
        pass
    elif command.type == 'A_COMMAND':
        return command.bincode
    else:  # C_COMMAND
        prefix = '111'
        comp = symbol.comp[command.comp]
        dest = symbol.dest[command.dest]
        jump = symbol.jump[command.jump]
        return prefix + comp + dest + jump
