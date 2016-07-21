from library import *
import bond_trade

def main():
    connect_to_prod()
    while True:
        msg = get_message()
        bond_trade.bond_trade(msg)
main()
