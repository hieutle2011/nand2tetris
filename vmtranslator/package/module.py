def handle_line(line):
    if line.startswith('//') or line in ['\n', '\r\n', '']:
        return None
    else:
        return line.lstrip().split()
