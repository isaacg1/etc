from library import *

BOND_PRICE = 1000
BOND_ALLOWED = 100

position = 0

def bond_trade(book):
    global position
    if book[SYMBOL] != BOND:
        return
    other = book[BUY]
    if other:
        best_bid = other[0]
        if best_bid[0] > BOND_PRICE:
            max_allowed = min(position - BOND_ALLOWED, best_bid[1])
            id, order = create_add_order(BOND, SELL, BOND_PRICE, max_allowed)
            send_order(order, EXCHANGE)
            position -= max_allowed
    other = book[SELL]
    if other:
        best_offer = other[0]
        if best_offer[0] < BOND_PRICE:
            max_allowed = min(BOND_ALLOWED - position[BOND], best_offer[1])
            id, order = create_add_order(BOND, BUY, BOND_PRICE, max_allowed)
            send_order(order, EXCHANGE)
            position += max_allowed
