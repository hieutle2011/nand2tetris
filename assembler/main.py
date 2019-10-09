from package.module import Symbol, Parser, Command, generate_binary_code
import sys


def main():
    fname = sys.argv[1]
    symbol = Symbol()
    asm = Parser(fname)

    # First pass: Add the label symbol
    for line in asm.lines:
        # Contruct each command
        c = Command(line)

        # Scan to add variables to symbol table
        if c.type == 'L_COMMAND' and not symbol.contains(c.symbol):
            symbol.addEntry(c.symbol, symbol.running_num)
        else:
            symbol.incre_running_num()

    # create file to write
    file = open(asm.hack_path, 'w')

    # Second pass: Add the variable symbol
    for line in asm.lines:
        command = Command(line)

        if command.type == 'L_COMMAND':
            pass
        elif command.type == 'C_COMMAND':
            code = generate_binary_code(command, symbol)
            file.write(code + '\n')
        # handle variables
        else:
            # @3
            if command.symbol == '':
                code = generate_binary_code(command, symbol)
                file.write(code + '\n')
            # @var in symbol
            elif not command.symbol == '' and symbol.contains(command.symbol):
                value = symbol.getAddress(command.symbol)
                command = Command('@'+str(value))

                code = generate_binary_code(command, symbol)
                file.write(code + '\n')
            else:  # new symbol
                symbol.addEntry(command.symbol, symbol.current_addr)
                command = Command('@' + str(symbol.current_addr))

                code = generate_binary_code(command, symbol)
                file.write(code + '\n')
                symbol.incre_current_addr()

    file.close()
    print("Done! New file is {}".format(asm.hack_path))


if __name__ == "__main__":
    main()
