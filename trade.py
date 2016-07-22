from library import *
from bond_trade import start, bond_trade2
from penny import create_penny

start_funcs = [start]
message_reactions = [bond_trade2,
        create_penny(library.XFL, 20, 1)]

def start_trading():
    for f in start_funcs:
        f()
    while True:
        msg = get_message()
        for reaction in message_reactions:
            reaction(msg)



