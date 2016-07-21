from library import *

DESIRED_EDGE = 5
ALLOWED = 10

vale_fair = 0
vale_pos = 0
vale_buy_size = 0
vale_sell_size = 0

valbz_pos = 0
valbz_buy_size = 0
valbz_sell_size = 0

ids = []

def start():
    pass
    
def trade(msg):
    global vale_fair
    if msg['type'] == 'book':
        if msg['symbol'] == 'VALBZ':
            if msg['buy'] and msg['sell']:
                buy = msg['buy'][0][0]
                sell = msg['sell'][0][0]
                fair = (buy + sell)/2
                vale_fair = fair
                update_vale()
                return True
    if msg['type'] == 'fill':
        if msg['symbol'] == 'VALE':
            print('Got filled on VALE')
            if msg['dir'] == 'BUY':
                vale_pos += msg['size']
                vale_buy_size -= msg['size']
            elif msg['dir'] == 'SELL':
                vale_pos += msg['size']
                vale_sell_size -= msg['size']
            else:
                print('Afase')
            update_vale()
            return True
    return False

def update_vale():
    global vale_pos
    global vale_buy_size
    global vale_sell_size
    if vale_fair == 0:
        return
    buy_price = vale_fair - DESIRED_EDGE
    sell_price = vale_fair + DESIRED_EDGE
    if ALLOWED - vale_pos > vale_buy_size:
        amount = ALLOWED - vale_pos - vale_buy_size
        id = send_buy_order(BOND, amount, buy_price)
        ids.append(id)
        vale_buy_size += amount
        print('vale', amount, buy_price)
    if ALLOWED + vale_pos > vale_sell_size:
        amount = ALLOWED + vale_pos - vale_sell_size
        id = send_sell_order(BOND, amount, buy_price)
        ids.append(id)
        vale_sell_size += amount
        print('vale', amount, sell_price)
    return
    
