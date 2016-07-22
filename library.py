from __future__ import print_function
import time
import json
import sys
import socket
import message_constants as mc
BUY = "BUY"
SELL = "SELL"
CANCEL = "cancel"

XLY= "XLY"
AMZN = "AMZN"
HD = "HD"
DIS = "DIS"

XLP = "XLP"
PG = "PG"
KO = "KO"
PM = "PM"

XLU = "XLU"
NEE = "NEE"
DUK = "DUK"
SO = "SO"

RSP = "RSP"

EXCHANGE = 0
_ID = 0

hello = None

id_to_symbol_map = {}
id_to_component_map = {}


def _get_new_id():
    global _ID
    _ID += 1
    return _ID

HELLO_MSG = json.dumps({"type" : "hello", "team" : "JIFFY"})

def _create_add_order(symbol, buy_or_sell, size, price):
    idd = _get_new_id()
    order = {"type": "add", "order_id": idd, "symbol": symbol, "dir": buy_or_sell, "price": price, "size": size}
    return json.dumps(order), idd

def _create_convert(symbol, size, buy_or_sell):
    idd = _get_new_id()
    order = {"type": "convert", "order_id": idd, "symbol": symbol, "dir": buy_or_sell, "size": size}
    return json.dumps(order), idd

def _create_buy_order(symbol, size, price):
    return _create_add_order(symbol, BUY, size, price)

def _create_sell_order(symbol, size, price):
    return _create_add_order(symbol, SELL, size, price)

def connect_to_test():
    print("CONNECTING TO TEST EXCHANGE")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("test-exch-jiffy", 25000))
    global EXCHANGE
    EXCHANGE =  s.makefile('w+', 1)
    send_message(HELLO_MSG)
    global hello
    hello = get_message()
    print(hello)

def connect_to_test2():
    print("CONNECTING TO TEST EXCHANGE")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("test-exch-jiffy", 25001))
    global EXCHANGE
    EXCHANGE =  s.makefile('w+', 1)
    send_message(HELLO_MSG)
    print(get_message())

def connect_to_prod():
    print("CONNECTING TO PROD EXCHANGE")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("production", 25000))
    global EXCHANGE
    EXCHANGE =  s.makefile('w+', 1)
    send_message(HELLO_MSG)
    print(get_message())

def send_message(order):
    #print("->" + str(order), file=sys.stderr)
    print(order, file=EXCHANGE)
    time.sleep(0.01)

def send_sell_order(symbol, size, price, component_name):
    order, id = _create_sell_order(symbol, size, price)
    id_to_symbol_map[id] = (symbol, size, price, SELL)
    id_to_component_map[id]=component_name
    send_message(order)
    return id

def send_buy_order(symbol, size, price, component_name):
    order, id = _create_buy_order(symbol, size, price)
    id_to_symbol_map[id] = (symbol, size, price, BUY)
    id_to_component_map[id]=component_name
    send_message(order)
    return id

def send_cancel_order(id):
    o = { "type" : CANCEL, "order_id" : id}
    s = json.dumps(o)
    send_message(s)

def send_convert_order(symbol, size, dir, component_name):
    order, id = _create_convert(symbol, size, dir)
    id_to_symbol_map[id] = (symbol, size, dir)
    id_to_component_map[id]=component_name
    send_message(order)
    return id

def get_message():
    s = EXCHANGE.readline().strip()
    if s == "":
        print("Round ended")
        sys.exit(0)
    #print("<-" + s, file=sys.stderr)
    o = json.loads(s)
    _print_fills(o)
    return o

_global_cash_position = 0

def _print_fills(msg):
  if msg[mc.TYPE] == mc.FILL:
    id = msg[mc.ORDER_ID]
    price = msg[mc.PRICE]
    size = msg[mc.SIZE]
    value = price * size
    if msg[mc.DIR] == BUY:
        value = value * -1
    _global_cash_position += value
    obj = {"log_type"  : "fill_log",
           "component" : id_to_component_map[id],
           "symbol"    : msg[mc.SYMBOL],
           #"order_info": id_to_symbol_map[id],
           "dir"       : msg[mc.DIR],
           "price"     : price,
           "size"      : size,
           "value"     : value,
           "cash"      : _global_cash_position
           }
    print(json.dumps(obj), file=sys.stderr)
