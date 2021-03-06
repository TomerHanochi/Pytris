from enum import Enum


class Key(Enum):
    """ Enum for keyboard keys and their corresponding pygame ids. """

    @classmethod
    def has_value(cls, value: int) -> bool:
        return any(item.value == value for item in cls)

    LEFT_SHIFT = 1
    RIGHT_SHIFT = 2
    SHIFT = 3
    BACKSPACE = 8
    TAB = 9
    RETURN = 13
    ESCAPE = 27
    SPACE = 32
    ZERO = 48
    ONE = 49
    TWO = 50
    THREE = 51
    FOUR = 52
    FIVE = 53
    SIX = 54
    SEVEN = 55
    EIGHT = 56
    NINE = 57
    LEFT_CTRL = 64
    LEFT_BRACKET = 91
    RIGHT_BRACKET = 93
    A = 97
    B = 98
    C = 99
    D = 100
    E = 101
    F = 102
    G = 103
    H = 104
    I = 105
    J = 106
    K = 107
    L = 108
    M = 109
    N = 110
    O = 111
    P = 112
    Q = 113
    R = 114
    S = 115
    T = 116
    U = 117
    V = 118
    W = 119
    X = 120
    Y = 121
    Z = 122
    DELETE = 127
    RIGHT_CTRL = 128
    CTRL = 192
    LEFT_ALT = 256
    RIGHT_ALT = 512
    ALT = 768
    CAPS = 8192
    CAPSLOCK = 1073741881
    F1 = 1073741882
    F2 = 1073741883
    F3 = 1073741884
    F4 = 1073741885
    F5 = 1073741886
    F6 = 1073741887
    F7 = 1073741888
    F8 = 1073741889
    F9 = 1073741890
    F10 = 1073741891
    F11 = 1073741892
    F12 = 1073741893
    RIGHT_ARROW = 1073741903
    LEFT_ARROW = 1073741904
    DOWN_ARROW = 1073741905
    UP_ARROW = 1073741906
