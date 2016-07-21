import library
BOND_PRICE = 1000
BOND_ALLOWED = 100
SYMBOL = 'symbol'
BOOK = 'book'
TYPE = 'type'
BUY = 'buy'
SELL ='sell'
FILL ='fill'
DIR = 'dir'
ACK = 'ack'
REJECT = 'reject'
ORDER_ID = 'order_id'

SYMBOL_PENNIED = library.VALBZ

def get_symbol_from_map_tuple(t):
    return t[0]

def is_it_my_order(msg):
    id = msg[ORDER_ID]
    tup = library.id_to_symbol_map[id]
    return get_symbol_from_map_tuple(t) == SYMBOL_PENNIED


def on_start():
    pass

def penny_valbz(msg):
    if msg[TYPE] == BOOK and msg[SYMBOL] == SYMBOL_PENNIED:
        buy = msg[BUY]
        sell = msg[SELL]
        penny_valbz_handle_book(buy, sell)
    if msg[TYPE] == ACK:
        if is_it_my_order(msg):
            penny_valbz_handle_ack(msg)
    if msg[TYPE] == REJECT:
        if is_it_my_order(msg):
            penny_valbz_handle_reject(msg)
    if msg[TYPE] == FILL:
        if is_it_my_order(msg):
            penny_valbz_handle_fill(msg)

def penny_valbz_handle_book(buy, sell):
    print("valbz_book")
    pass

def penny_valbz_handle_reject(id, tup, msg):
    print("valbz_reject")
    pass

def penny_valbz_handle_ack(id, order):
    print("valbz_ack")
    pass

def penny_valbz_handle_book(buy, sell):
    print("valbz_book")
    pass
