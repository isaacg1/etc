from library import *
import bond_trade

def main():
    connect_to_test()
    send_message(-1, create_buy_order(999999, BOND,  1, 999))
    while True:
        msg = get_message()
        print("got msg")
        print(json.dumps(msg))
        bond_trade.bond_trade(msg)
        print("bond_trade finished")
main()
