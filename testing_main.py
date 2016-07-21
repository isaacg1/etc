from __future__ import print_function
from library import *
import bond_trade
import sys

def main():
    connect_to_test()
    send_message(create_buy_order(BOND,  1, 999))
    while True:
        msg = get_message()
        print("got msg", file=sys.stderr)
        print(json.dumps(msg), file=sys.stderr)
        bond_trade.bond_trade(msg)
        print("bond_trade finished", file=sys.stderr)
main()
