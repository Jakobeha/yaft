#!/usr/bin/python3 -B

import sys

def read_header(file):
    line = file.readline()
    assert line != '', 'Bad file; bad header'
    at_end = line.startswith('static const struct glyph_t glyphs[] = {')
    return (at_end, line)

def read_glyph_line(file):
    while True:
        line = file.readline()
        assert line != '', 'Bad file; no footer'
        if line.startswith('};'):
            return None
        assert line.lstrip().startswith('{'), 'Bad file; no glyph entry'
        number = int(line.lstrip()[1:line.index(',') - 1])
        # Doesn't actually have this entry, empty is replaced by the default so it's
        # redundant. UNLESS it's U+0020 or U+3000, which ARE the defaults
        if line.rstrip().endswith(', {0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0'\
            ', 0x0, 0x0, 0x0, 0x0}},') and number not in [0x0020, 0x3000]:
            continue
        return (number, line)

def run(paths):
    files = [open(p, 'r') for p in paths]
    # Print header of first file, and assert the others' headers are the same
    while True:
        (main_at_end, main_line) = read_header(files[0])
        print(main_line, end='')
        for f in files[1:]:
            (at_end, line) = read_header(f)
            assert main_line == line and main_at_end == at_end,\
                'Files have different headers'
        if main_at_end:
            break
    # Read each glyph entry and print in order of their number,
    # priotizing the entry from the earlier file when the number is the same
    next_lines = [read_glyph_line(f) for f in files]
    while any(line is not None for line in next_lines):
        best_number = sys.maxsize
        best_line = None
        for line in next_lines:
            if line is not None and line[0] < best_number:
                best_number = line[0]
                best_line = line[1]

        print(best_line, end='')
        for i in range(len(next_lines)):
            line = next_lines[i]
            if line is not None and line[0] == best_number:
                next_lines[i] = read_glyph_line(files[i])
    # Print footer
    print('};')
    # Close files
    for f in files:
        f.close()


if __name__ == '__main__':
    run(sys.argv[1:])
