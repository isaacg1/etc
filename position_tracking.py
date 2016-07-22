from __future__ import print_function
import sys
cash = 0
sym_to_pos = {}
sym_to_book = {}
sym_to_bid_size = {}
sym_to_offer_size = {}

partial_fills = {}

ALL_SYMBOLS = ["XLY", "AMZN", "HD", "DIS", "XLP", "PG", "KO",
                "PM", "XLU", "NEE", "DUK", "SO", "RSP"]


for symbol in ALL_SYMBOLS:
    sym_to_pos[symbol] = 0
    sym_to_bid_size[symbol] = 0
    sym_to_offer_size[symbol] = 0        
def on_hello(msg):
    global cash
    assert msg['type'] == 'hello'
    cash = msg['cash']
    for val in msg['symbols']:
        symbol = val['symbol']
        pos = val['position']
        sym_to_pos[symbol] = pos
        sym_to_bid_size[symbol] = 0
        sym_to_offer_size[symbol] = 0

def on_fill(msg):
    global cash
    assert msg['type'] == 'fill'
    symbol = msg['symbol']
    dir = msg['dir']
    price = msg['price']
    size = msg['size']
    if dir == 'BUY':
        cash -= price * size
        sym_to_pos[symbol] += size
        sym_to_bid_size[symbol] -= size
    elif dir == 'SELL':
        cash += price * size
        sym_to_pos[symbol] -= size
        sym_to_offer_size[symbol] -= size
    else:
        assert False
    partial_fills[msg['order_id']] = partial_fills.get(msg['order_id'], 0) + size
    buy = (sym_to_book[symbol]['buy'] or [[None, None]])[0][0]
    sell = (sym_to_book[symbol]['sell'] or [[None, None]])[0][0]
    spread = sell - buy if buy and sell else None
    print('Symbol: %s; Pos: %s; Bid size: %s; Offer size: %s; Best Bid: %s: Best Offer: %s; Best_spread: %s' %
            (symbol, sym_to_pos[symbol], sym_to_bid_size[symbol],
                sym_to_offer_size[symbol], buy, sell,
                spread), file=sys.stderr)
           
    return

def on_ack(msg, id_to_symbol_map):
    assert msg['type'] == 'ack'
    order = id_to_symbol_map[msg['order_id']]
    if len(order) == 4:
        # add order
        symbol, size, price, dir = order
        if dir == 'BUY':
            sym_to_bid_size[symbol] += size
        elif dir == 'SELL':
            sym_to_offer_size[symbol] += size
        else:
            assert False
    elif len(order) == 3:
        # convert
        # (symbol, size, dir)
        pass
    else:
        assert False

def on_out(msg, id_to_symbol_map):
    assert msg['type'] == 'out'
    order = id_to_symbol_map[msg['order_id']]
    if len(order) == 4:
        symbol, size, price, dir = order
        if dir == 'BUY':
            sym_to_bid_size[symbol] -= size
            - partial_fills.get(msg['order_id'], 0)
        elif dir == 'SELL':
            sym_to_offer_size[symbol] -= size
            - partial_fills.get(msg['order_id'], 0)
        else:
            assert False
    partial_fills[msg['order_id']] = 0

def on_book(msg):
    assert msg['type'] == 'book'
    symbol = msg['symbol']
    sym_to_book[symbol] = msg
     
def on_msg(msg, id_to_symbol_map):
    type = msg['type']
    if type == 'ack':
        on_ack(msg, id_to_symbol_map)
    elif type == 'fill':
        on_fill(msg)
    elif type == 'out':
        on_out(msg, id_to_symbol_map)
    elif type == 'book':
        on_book(msg)
    elif type == 'hello':
        on_hello(msg)