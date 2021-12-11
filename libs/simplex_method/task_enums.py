from enum import IntEnum


class Sign(IntEnum):
    LEQ = 3
    EQ = 2
    GEQ = 1
    UNKNOWN = 4

    @staticmethod
    def from_string(string):
        if string == '=':
            return Sign.EQ
        elif string == '>=':
            return Sign.GEQ
        elif string == '<=':
            return Sign.LEQ
        else:
            return Sign.UNKNOWN


class Extremum(IntEnum):
    MIN = 1
    MAX = 2
    UNKNOWN = 3

    @staticmethod
    def from_string(string: str):
        if string.lower() == 'min':
            return Extremum.MIN
        elif string.lower() == 'max':
            return Extremum.MAX
        else:
            return Extremum.UNKNOWN
