from library import *
from position_tracking import *
import time
XLY_group = {XLY : 20, AMZN : -6, HD : -6, DIS : -8}

OFFSET = 0.1
CONVERT_AMOUNT = 20

last_time = 0


def create_convert(symbols_to_weights, main_symbol):
    STW = symbols_to_weights
    MAIN = main_symbol
    NAME = "CONVERT " + MAIN

    def convert(_msg):
        global last_time
        global is_converting
        now = time.clock()
        if now < last_time + OFFSET:
            return
        last_time = now
        amount_long = 0
        for symbol in STW:
            amount_long += sym_to_pos[symbol] / STW[symbol]
        if not is_converting and abs(amount_long) > 4:
            print("Time to convert: %s" % amount_long)
            dir = 'BUY' if amount_long < 0 else 'SELL'
            size = CONVERT_AMOUNT * int(abs(amount_long) / 4)
            my_id = send_convert_order(MAIN, size, dir, NAME)
        print('checked')
    return convert

            
