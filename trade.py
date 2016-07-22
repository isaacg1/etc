from library import *
import pennying_trade
#import position_tracking

start_funcs = []
message_reactions = pennying_trade.etf_pennies + pennying_trade.stock_pennies

def start_trading():
    for f in start_funcs:
        f()
    while True:
        msg = get_message()
        #position_tracking.on_msg(msg)
        for reaction in message_reactions:
            reaction(msg)



