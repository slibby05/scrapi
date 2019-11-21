
class ParseException(Exception):
    def __init__(self, row, col, expected, got):
        self.row = row
        self.col = col
        self.expected = expected
        self.got = got
    def __str__(self):
        return "Error at row %d col %d: expected %s, but got %s" % (self.row, self.col, self.expected, self.got)

class LexException(Exception):
    def __init__(self, row, col, got):
        self.row = row
        self.col = col
        self.got = got
    def __str__(self):
        return "Error at row %d col %d: invalid symbol %c" % (self.row, self.col, self.got)
