from library import *
from bond_trade import start, bond_trade2
import val_trade
import valbz_trade
import ms_penny
import gs_penny
import wfc_penny
import xlf_penny
import adr_trade

start_funcs = [adr_trade.start]
message_reactions= [adr_trade.trade]

def start_trading():
    for f in start_funcs:
        f()
    while True:
        msg = get_message()
        for reaction in message_reactions:
            reaction(msg)



