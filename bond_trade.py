from library import *

BOND_PRICE = 1000
BOND_ALLOWED = 100
SYMBOL = 'symbol'
BOOK = 'book'


position = 0
id = 0

def bond_trade(book):
    global position
    global id
    if book[TYPE] != BOOK:
        return
    if book[SYMBOL] != BOND:
        return
    other = book[BUY]
    if other:
        best_bid = other[0]
        if best_bid[0] > BOND_PRICE:
            max_allowed = min(position - BOND_ALLOWED, best_bid[1])
            order = create_sell_order(id, BOND, BOND_PRICE, max_allowed)
            id += 1
            send_order(order, EXCHANGE)
            print("sent order to buy %s", max_allowed)
            position -= max_allowed
    other = book[SELL]
    if other:
        best_offer = other[0]
        if best_offer[0] < BOND_PRICE:
            max_allowed = min(BOND_ALLOWED - position[BOND], best_offer[1])
            order = create_buy_order(id, BOND, BOND_PRICE, max_allowed)
            id += 1
            send_order(order, EXCHANGE)
            print("sent order to sell %s", max_allowed)
            position += max_allowed
