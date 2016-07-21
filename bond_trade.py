from library import *

BOND_PRICE = 1000
BOND_ALLOWED = 100
SYMBOL = 'symbol'
BOOK = 'book'
TYPE = 'type'
BUY = 'buy'
SELL ='sell'


position = 0
id = 0

def bond_trade(book):
    global position
    global id
    if book[TYPE] == BOOK and book[SYMBOL] == BOND:
        other = book[BUY]
        if other:
            best_bid = other[0]
            if best_bid[0] > BOND_PRICE:
                max_allowed = min(position - BOND_ALLOWED, best_bid[1])
                if max_allowed > 0:
                    order = create_sell_order(id, BOND, BOND_PRICE, max_allowed)
                    id += 1
                    send_message(order)
                    print("sent order to buy %s", max_allowed)
        other = book[SELL]
        if other:
            best_offer = other[0]
            if best_offer[0] < BOND_PRICE:
                max_allowed = min(BOND_ALLOWED - position, best_offer[1])
                if max_allowed > 0:
                    order = create_buy_order(id, BOND, BOND_PRICE, max_allowed)
                    id += 1
                    send_message(order)
                    print("sent order to sell %s", max_allowed)
        return
    if book[TYPE] == FILL and book[SYMBOL] == BOND:
        if book[DIR] == BUY:
            position += book[SIZE]
        if book[DIR] == SELL:
            position -= book[SIZE]
