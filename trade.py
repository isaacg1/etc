from library import *
from bond_trade import start, bond_trade2
import val_trade
import valbz_trade
import ms_penny
import gs_penny
import wfc_penny
import xlf_penny

start_funcs = [start]
message_reactions= [val_trade.penny_valbz, bond_trade2,
        valbz_trade.penny_valbz, ms_penny.penny_valbz, gs_penny.penny_valbz,
        wfc_penny.penny_valbz, xlf_penny.penny_valbz]

def start_trading():
    for f in start_funcs:
        f()
    while True:
        msg = get_message()
        for reaction in message_reactions:
            reaction(msg)



