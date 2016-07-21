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

BUY_PRICE = 999
SELL_PRICE = 1001
pos = 0
buy_size = 0
sell_size = 0
my_ids = []

def start():
    global my_ids
    global buy_size
    global sell_size
    id1 = send_buy_order(BOND, 100, BUY_PRICE)
    id2 = send_sell_order(BOND, 100, SELL_PRICE)
    buy_size += 100
    sell_size += 100
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
        if msg['symbol'] == 'BOND':
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
                id = send_buy_order(BOND, amount, BUY_PRICE)
                my_ids.append(id)
                buy_size += amount
                print(BOND, amount, BUY_PRICE)
            if pos + BOND_ALLOWED > sell_size:
                amount = pos + BOND_ALLOWED - sell_size
                id = send_sell_order(BOND, amount, SELL_PRICE)
                my_ids.append(id)
                sell_size += amount
                print(BOND, amount, SELL_PRICE)
            print(pos, buy_size, sell_size)
            return True
    return False
