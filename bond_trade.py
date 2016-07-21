from library import *

BOND_PRICE = 1000
BOND_ALLOWED = 100
SYMBOL = 'symbol'
BOOK = 'book'
TYPE = 'type'
BUY = 'buy'
SELL ='sell'
FILL ='fill'
DIR = 'dir'

position = 0

def bond_trade(book):
    global position
    if book[TYPE] == BOOK and book[SYMBOL] == BOND:
        other = book[BUY]
        if other:
            best_bid = other[0]
            if best_bid[0] > BOND_PRICE:
                max_allowed = min(position - BOND_ALLOWED, best_bid[1])
                if max_allowed > 0:
                    order, id = create_sell_order(BOND, BOND_PRICE, max_allowed)
                    send_message(order)
                    print("sent order to buy %s", max_allowed)
        other = book[SELL]
        if other:
            best_offer = other[0]
            if best_offer[0] < BOND_PRICE:
                max_allowed = min(BOND_ALLOWED - position, best_offer[1])
                if max_allowed > 0:
                    order = create_buy_order(BOND, BOND_PRICE, max_allowed)
                    send_message(order)
                    print("sent order to sell %s", max_allowed)
        return
    if book[TYPE] == FILL and book[SYMBOL] == BOND:
        print("position")
        if book[DIR] == "BUY":
            position += book[SIZE]
        elif book[DIR] == "SELL":
            position -= book[SIZE]
        else:
            print("bug happened on a fill")


BUY_PRICE = 997
SELL_PRICE = 1003
pos = 0
buy_size = 100
sell_size = 100

def start():
    create_buy_order(BOND, BUY_PRICE, 100)
    create_sell_order(BOND, SELL_PRICE, 100)

def bond_trade2(msg):
    global pos
    global buy_size
    global sell_size
    if msg['type'] == 'reject':
        print('Got rejected\n', msg)
        # NEED TO DO SOMETHING TO CHECK ID
    elif msg['type'] == 'fill':
        print('Got filled')
        print(pos, buy_size, sell_size
        if msg['dir'] == 'BUY':
            pos += msg['size']
            buy_size -= msg['size']
        elif msg['dir'] == 'SELL':
            pos -= msg['size']
            sell_size -= msg['size']
        else:
            print("Something broke")
        if BOND_ALLOWED - pos > buy_size:
            amount = BOND_ALLOWED - pos - buy_size
            create_buy_order(BOND, BUY_PRICE, amount)
            buy_size += amount
        if pos + BOND_ALLOWED > sell_size:
            amount = pos + BOND_ALLOWED - sell_size
            create_sell_order(BOND, SELL_PRICE, amount)
            sell_size += amount
        return True
    
