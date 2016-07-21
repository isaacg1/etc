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


BUY_PRICE = 999
SELL_PRICE = 1001
pos = 0
buy_size = 0
sell_size = 0
my_ids = []

def start():
    global my_ids
    id1 = send_buy_order(BOND, 100, BUY_PRICE)
    id2 = send_sell_order(BOND, 100, SELL_PRICE)
    my_ids.extend([id1, id2])

def bond_trade2(msg):
    global pos
    global buy_size
    global sell_size
    global my_ids
    if msg['type'] == 'open':
        print('hi')
        start()
        print(pos, buy_size, sell_size)
        return True
    if msg['type'] == 'reject':
        print('Got redjected\n', msg)
        if msg['order_id'] in my_ids:
            symbol, size, price, type = id_to_symbol_map[msg['order_id']]
            if type == 'BUY':
                buy_size -= size
            elif type == 'SELL':
                sell_size -= size
            else:
                print(type)
            print(pos, buy_size, sell_size)
            return True
        return False
            
    elif msg['type'] == 'fill':
        print('Got filled')

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
            send_buy_order(BOND, amount, BUY_PRICE)
            buy_size += amount
            print(BOND, amount, BUY_PRICE)
        if pos + BOND_ALLOWED > sell_size:
            amount = pos + BOND_ALLOWED - sell_size
            send_sell_order(BOND, amount, SELL_PRICE)
            sell_size += amount
            print(BOND, amount, SELL_PRICE)
        print(pos, buy_size, sell_size)
        return True
    return False
