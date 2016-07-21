from library import *

BOND_PRICE = 1000
BOND_ALLOWED = 100

def bond_trade(book, position):
    if book[BOND].other.bid:
        best_bid = book[BOND].other.buy[0]
        if best_bid > BOND_PRICE:
            max_allowed = position[BOND] - BOND_ALLOWED
            id, order = create_add_order(BOND, SELL, BOND_PRICE, max_allowed)
            out.append(id, order)
    if book[BOND].other.offer:
        best_offer = book[BOND].other.offer[0]
        if best_offer < BOND_PRICE:
            max_allowed = BOND_Allowed - position[BOND]
            id, order = create_add_order(BOND, BUY, BOND_PRICE, max_allowed)
