from __future__ import print_function
from library import *
import bond_trade
import sys
import trade

def main():
    connect_to_test()
    send_message(create_buy_order(BOND,  1, 999))
    trade.start_trading()

main()
