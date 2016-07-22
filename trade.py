from library import *
import pennying_trade
import position_tracking
import adjusting_trade
import scaling_trade
import convert
start_funcs = []
message_reactions = pennying_trade.etf_pennies + pennying_trade.stock_pennies\
+ scaling_trade.scales + [convert.create_convert(convert.XLY_group, XLY)]
def start_trading():
    for f in start_funcs:
        f()
    while True:
        msg = get_message()
        position_tracking.on_msg(msg, id_to_symbol_map)
        for reaction in message_reactions:
            reaction(msg)



