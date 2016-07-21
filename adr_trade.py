from library import *

DESIRED_EDGE = 5
ALLOWED = 10
CONVERT_LIMIT = 7
CONVERT_AMOUNT = 10

vale_fair = 0
vale_pos = 0
vale_buy_size = 0
vale_sell_size = 0

valbz_pos = 0
vale_buy_size = 0
vale_sell_size = 0

ids = []

def start():
    from library import hello
    print(hello)
    for entry in hello['symbols']:
        if entry['symbol'] == 'VALE':
            vale_pos = entry['position']
        elif entry['symbol'] == 'VALBZ':
            valbz_pos = entry['position']
    pass
    
def trade(msg):
    global vale_fair
    global vale_pos
    global vale_buy_size
    global vale_sell_size
    if msg['type'] == 'book':
        if msg['symbol'] == 'VALBZ':
            if msg['buy'] and msg['sell']:
                buy = msg['buy'][0][0]
                sell = msg['sell'][0][0]
                fair = (buy + sell)/2
                vale_fair = fair
                update_vale()
                return True
    elif msg['type'] == 'fill':
        if msg['symbol'] == 'VALE':
            print('Got filled on VALE')
            if msg['dir'] == 'BUY':
                vale_pos += msg['size']
                vale_buy_size -= msg['size']
            elif msg['dir'] == 'SELL':
                vale_pos -= msg['size']
                vale_sell_size -= msg['size']
            else:
                print('Afase')
            
        if msg['symbol'] == VALBZ:
            print('Got filled on VALBZ')
            if msg['dir'] == 'BUY':
                valbz_pos += msg['size']
                vale_buy_size -= msg['size']
            elif msg['dir'] == 'SELL':
                valbz_pos -= msg['size']
                valbz_sell_size -= msg['size']
            else:
                print('Afase')
            return True
    elif msg['type'] == 'reject':
        if msg['order_id'] in ids:
            print('got_rejected', msg)
            symbol, size, price, type = id_to_symbol_map[msg['order_id']]
            if symbol == VALE:
                if type == 'BUY':
                    vale_buy_size -= size
                elif type == 'SELL':
                    vale_sell_size -= size
                else:
                    print('asdfas')
            elif symbol == VALBZ:
                if type == 'BUY':
                    valbz_buy_size -= size
                elif type == 'SELL':
                    valbz_sell_size -= size
                else:
                    print('zbasdfas')
            print('valbz', valbz_pos, valbz_buy_size, valbz_sell_size)
            return True
        return False
    return False

def update_vale():
    global vale_pos
    global vale_buy_size
    global vale_sell_size
    global valbz_pos
    if vale_fair == 0:
        return
    if vale_pos > CONVERT_LIMIT:
        if ALLOWED - valbz_pos > 5:
            amount = min(CONVERT_AMOUNT, ALLOWED - valbz_pos)
            id = send_convert_order(VALE, amount, SELL)
            print("CONVERTED SELL VALE")
            vale_pos -= amount
            valbz_pos += amount
            id2 = send_sell_order(VALBZ, amount, vale_fair)
            ids.append(id2)
            valbz_sell_size += amount
    if vale_pos < -CONVERT_LIMIT:
        if ALLOWED + valbz_pos > 5:
            amount = min(CONVERT_AMOUNT, ALLOWED + valbz_pos)
            id = send_convert_order(VALE, amount, BUY)
            print("CONVERTED BUY VALE")
            vale_pos += amount
            valbz_pos -= amount
            id2 = send_buy_order(VALBZ, amount, vale_fair)
            ids.append(id2)
            valbz_buy_size += amount
    buy_price = vale_fair - DESIRED_EDGE
    sell_price = vale_fair + DESIRED_EDGE
    if ALLOWED - vale_pos > vale_buy_size:
        amount = ALLOWED - vale_pos - vale_buy_size
        id = send_buy_order(VALE, amount, buy_price)
        ids.append(id)
        vale_buy_size += amount
        print('buy', VALE, amount, buy_price)
    if ALLOWED + vale_pos > vale_sell_size:
        amount = ALLOWED + vale_pos - vale_sell_size
        id = send_sell_order(VALE, amount, sell_price)
        ids.append(id)
        vale_sell_size += amount
        print('sell', VALE, amount, sell_price)
    return
    
