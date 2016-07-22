from library import *
from position_tracking import *
import time
XLY_group = {XLY : 20, AMZN : -6, HD : -6, DIS : -8}
XLP_group = {XLP : 20, PG : -12, KO : -12, PM : -6}
XLU_group = {XLU : 20, NEE : -8, DUK : -6, SO : -8}

OFFSET = 0.1
CONVERT_AMOUNT = 20

last_time = 0


def create_convert(symbols_to_weights, main_symbol):
    STW = symbols_to_weights
    MAIN = main_symbol
    NAME = "CONVERT " + MAIN

    def convert(_msg):
        global last_time
        now = time.clock()
        if now < last_time + OFFSET:
            return
        last_time = now
        amount_long = 0
        for symbol in STW:
            amount_long += sym_to_pos[symbol] / float(STW[symbol])
        if abs(amount_long) > 4:
            dir = 'BUY' if amount_long < 0 else 'SELL'
            size = CONVERT_AMOUNT * int(abs(amount_long) / 4)
            print("Time to convert: %s, %s, %s" % (MAIN, size, dir))
            my_id = send_convert_order(MAIN, size, dir, NAME)
    return convert

            
trades = [create_convert(XLY_group, XLY), create_convert(XLP_group, XLP),
        create_convert(XLU_group, XLU)]
