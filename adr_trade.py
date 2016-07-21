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
valbz_buy_size = 0
valbz_sell_size = 0

ids = []

waiting_for_ack

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
    global valbz_pos
    global valbz_buy_size
    global valbz_sell_size
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
                valbz_buy_size -= msg['size']
            elif msg['dir'] == 'SELL':
                valbz_pos -= msg['size']
                valbz_sell_size -= msg['size']
            else:
                print('Afase')
            return True
    elif msg['type'] == 'reject':
        if msg['order_id'] in ids:
            print('got_rejected', msg)
            print('vale', vale_pos, vale_buy_size, vale_sell_size, 'valbz', valbz_pos, valbz_buy_size, valbz_sell_size)
            print(id_to_symbol_map[msg['order_id']])
            return True
    elif msg['type'] == 'ack':
        if msg['order_id'] in ids:
            rsp = id_to_symbol_map[msg['order_id']]
            print('ack:' rsp)
            if len(rsp) == 4:
                symbol, size, price, dir = rsp
                if symbol == VALE:
                    if dir == BUY:
                        vale_pos += size
                        vale_buy_size += size
                    elif dir == SELL:
                        vale_pos -= size
                        vale_sell_size += size
                if symbol == VALBZ:
                    if dir == BUY:
                        valbz_pos += size
                        valbz_buy_size += size
                    elif dir == SELL:
                        valbz_pos -= size
                        valbz_sell_size += size
            if len(rsp) == 3:
                symbol, size, dir = rsp
                if symbol == VALE:
                    if dir == 'BUY':
                        valbz_pos -= size
                        vale_pos += size
                    if dir == 'SELL':
                        valbz_pos += size
                        vale_pos -= size
                        
        return False
    return False

def update_vale():
    global vale_pos
    global vale_buy_size
    global vale_sell_size
    global valbz_pos
    global valbz_buy_size
    global valbz_sell_size
    if vale_fair == 0:
        return
    if vale_pos > CONVERT_LIMIT:
        if ALLOWED - valbz_pos > 5:
            amount = min(CONVERT_AMOUNT, ALLOWED - valbz_pos)
            id = send_convert_order(VALE, amount, SELL)
            print('vale', vale_pos, vale_buy_size, vale_sell_size, 'valbz', valbz_pos, valbz_buy_size, valbz_sell_size)
            ids.append(id)
            print("CONVERTED SELL VALE")
            id2 = send_sell_order(VALBZ, amount, vale_fair)
            print('vale', vale_pos, vale_buy_size, vale_sell_size, 'valbz', valbz_pos, valbz_buy_size, valbz_sell_size)
            ids.append(id2)
    if vale_pos < -CONVERT_LIMIT:
        if ALLOWED + valbz_pos > 5:
            amount = min(CONVERT_AMOUNT, ALLOWED + valbz_pos)
            id = send_convert_order(VALE, amount, BUY)
            print('vale', vale_pos, vale_buy_size, vale_sell_size, 'valbz', valbz_pos, valbz_buy_size, valbz_sell_size)
            ids.append(id)
            print("CONVERTED BUY VALE")
            id2 = send_buy_order(VALBZ, amount, vale_fair)
            print('vale', vale_pos, vale_buy_size, vale_sell_size, 'valbz', valbz_pos, valbz_buy_size, valbz_sell_size)
            ids.append(id2)
    buy_price = vale_fair - DESIRED_EDGE
    sell_price = vale_fair + DESIRED_EDGE
    if ALLOWED - vale_pos > vale_buy_size:
        amount = ALLOWED - vale_pos - vale_buy_size
        id = send_buy_order(VALE, amount, buy_price)
        print('vale', vale_pos, vale_buy_size, vale_sell_size, 'valbz', valbz_pos, valbz_buy_size, valbz_sell_size)
        ids.append(id)
        print('buy', VALE, amount, buy_price)
    if ALLOWED + vale_pos > vale_sell_size:
        amount = ALLOWED + vale_pos - vale_sell_size
        id = send_sell_order(VALE, amount, sell_price)
        print('vale', vale_pos, vale_buy_size, vale_sell_size, 'valbz', valbz_pos, valbz_buy_size, valbz_sell_size)
        ids.append(id)
        print('sell', VALE, amount, sell_price)
    return
    
