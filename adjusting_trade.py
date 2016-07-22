from library import *
from position_adjusting import create_position_adjusting
from position_tracking import ALL_SYMBOLS


MAX_SPREAD = 6
MIN_ABS_POSITION = 30


trade = [ create_position_adjusting(symbol, MAX_SPREAD, MIN_ABS_POSITION) for
        symbol in ALL_SYMBOLS]
