from library import *
from bond_trade import start, bond_trade2
import val_trade

start_funcs = [start]
message_reactions= [bond_trade2, val_trade.penny_valbz]

def start_trading():
    for f in start_funcs:
        f()
    while True:
        msg = get_message()
        for reaction in message_reactions:
            reaction(msg)



