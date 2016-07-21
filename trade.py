from library import *
from bond_trade import start, bond_trade2

start_funcs = [start]
message_reactions= [bond_trade2]

def start_trading():
    for f in start_funcs:
        f()
    while True:
        msg = get_message()
        for reaction in message_reactions:
            reaction(msg)



