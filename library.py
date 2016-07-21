from __future__ import print_function
import json
import sys
import socket
BUY = "BUY"
SELL = "SELL"
BOND = "BOND"
VALBZ = "VALBZ"
VALE = "VALE"
GS = "GS"
MS = "MS"
WFC = "WFC"
XLF = "XLF"

EXCHANGE = 0
_ID = 0

hello = None

id_to_symbol_map = {}


def _get_new_id():
    global _ID
    _ID += 1
    return _ID

HELLO_MSG = json.dumps({"type" : "hello", "team" : "JIFFY"}) + "\n"

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
    print("->" + str(order), file=sys.stderr)
    print(order, file=EXCHANGE)

def send_sell_order(symbol, size, price):
    order, id = _create_sell_order(symbol, size, price)
    id_to_symbol_map[id] = (symbol, size, price, SELL)
    send_message(order)
    return id

def send_buy_order(symbol, size, price):
    order, id = _create_buy_order(symbol, size, price)
    id_to_symbol_map[id] = (symbol, size, price, BUY)
    send_message(order)
    return id

def send_convert_order(symbol, size, dir):
    order, id = _create_convert(symbol, size, dir)
    id_to_symbol_map[id] = (symbol, size, dir)
    send_message(order)
    return id

def get_message():
    s = EXCHANGE.readline().strip()
    if s == "":
        print("Round ended")
        sys.exit(0)
    print("<-" + s, file=sys.stderr)
    return json.loads(s)


