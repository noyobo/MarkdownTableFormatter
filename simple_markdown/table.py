import re
import unicodedata

import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    from_string = dict((key, value) for key, value in enums.items())
    from_int = dict((value, key) for key, value in enums.items())
    enums['from_string'] = from_string
    enums['from_int'] = from_int
    return type('Enum', (), enums)

Justify = enum("LEFT", "CENTER", "RIGHT")


## asian unicode characters might be wider than ascii
def has_fullwidth_char(text):
    for char in text:
        # F: Fullwidth, A: Ambiguous, W: Wide
        if unicodedata.east_asian_width(char) in "FWA":
            return True
    return False


def fullwidth(text):
    """ Convert to fullwidth characters via a mapping on ascii charset
    from http://stackoverflow.com/questions/4622357/how-to-control-padding-of-unicode-string-containing-east-asia-characters
    """
    # full width versions (SPACE is non-contiguous with ! through ~)
    SPACE = '\N{IDEOGRAPHIC SPACE}'
    EXCLA = '\N{FULLWIDTH EXCLAMATION MARK}'
    TILDE = '\N{FULLWIDTH TILDE}'

    # strings of ASCII and full-width characters (same order)
    west = ''.join(chr(i) for i in range(ord(' '),ord('~')))
    east = SPACE + ''.join(chr(i) for i in range(ord(EXCLA),ord(TILDE)))

    # build the translation table
    full = str.maketrans(west,east)
    return text.translate(full)


def find_all(text):
    tables = []
    offset = 0
    while True:
        grp = re.search(".*\|.*\r?\n[\s\t]*\|?(?::?[-. ]+:?\|)+(\r?\n.*\|.*)+",
                        text[offset:], re.MULTILINE)
        if grp is None:
            return tables
        tables.append((grp.start() + offset, grp.end() + offset))
        offset = offset + grp.end()
    return tables


def format(raw_table, margin=1, padding=0, default_justify=Justify.LEFT):
    fullwidth_table = False
    if has_fullwidth_char(raw_table):
        fullwidth_table = True
    rows = raw_table.splitlines()

    # add missing leading/trailing '|'
    for idx, row in enumerate(rows):
        if re.match("^[\s\t]*\|", row) is None:
            rows[idx] = "|" + rows[idx]
        if re.match(".*\|[\s\t]*\r?\n?$", row) is None:
            rows[idx] = rows[idx] + "|"
    matrix = [[col.strip() for col in row.split("|")] for row in rows]

    # remove first and last empty columns
    matrix[:] = [row[1:] for row in matrix]
    matrix[:] = [row[:-1] for row in matrix]

    # ensure there's same column number for each row or add missing ones
    col_cnt = max([len(row) for row in matrix])
    matrix[:] = \
        [r if len(r) == col_cnt else r + [""]*(col_cnt-len(r)) for r in matrix]

    # get each column justification
    justify = []
    matrix[1] = [re.sub("[-. ]+","-", col) for col in matrix[1]]
    for col_idx, col in enumerate(matrix[1]):
        if col.startswith(":") and col.endswith(":"):
            justify.append(Justify.CENTER)
        elif col.endswith(":"):
            justify.append(Justify.RIGHT)
        elif col.startswith(":"):
            justify.append(Justify.LEFT)
        else:
            justify.append(default_justify)

    # separation row is processed later
    matrix.pop(1)

    # convert all table to fullwidth if there's any fullwidth character
    if fullwidth_table:
        matrix = [[fullwidth(col) for col in row] for row in matrix]

    # get text size for each cell
    text_width = [[len(col) for col in row] for row in matrix]

    # determine column width (without padding and margin)
    col_width = [max(size) for size in zip(*text_width)]
    space_char = " "
    if fullwidth_table:
        space_char = fullwidth(" ")

    # update cells with justified text
    table = []
    for row in matrix:
        for col_idx, col in enumerate(row):
            if justify[col_idx] == Justify.CENTER:
                div, mod = divmod(col_width[col_idx] - len(col), 2)
                text = space_char * div + col + space_char * (div+mod)
            elif justify[col_idx] == Justify.RIGHT:
                text = col.rjust(col_width[col_idx], space_char)
            elif justify[col_idx] == Justify.LEFT:
                text = col.ljust(col_width[col_idx], space_char)
            # add padding
            if justify[col_idx] != Justify.CENTER:
                text = text + " " * padding
            row[col_idx] = " " * margin + text + " " * margin

    # build separation row
    sep_row = []
    for col_idx, col in enumerate(matrix[0]):
        if fullwidth_table:
            line = list("-" * (col_width[col_idx] * 2 + margin * 2))
        else:
            line = list("-" * (col_width[col_idx] + margin * 2))
        if justify[col_idx] != Justify.CENTER:
            line.extend(list("-" * padding))

        if justify[col_idx] == Justify.LEFT:
            line[0] = ":"
        elif justify[col_idx] == Justify.CENTER:
            line[0] = ":"
            line[-1] = ":"
        elif justify[col_idx] == Justify.RIGHT:
            line[-1] = ":"
        sep_row.append("".join(line))
    matrix.insert(1, sep_row)

    for row in matrix:
        table.append("|" + "|".join(row) + "|")
    return "\n".join(table)
