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

def get_new_id():
    global _ID
    _ID += 1
    return _ID

HELLO_MSG = json.dumps({"type" : "hello", "team" : "JIFFY"}) + "\n"

def create_add_order(symbol, buy_or_sell, size, price):
    idd = get_new_id()
    order = {"type": "add", "order_id": idd, "symbol": symbol, "dir": buy_or_sell, "price": price, "size": size}
    return json.dumps(order), idd

def create_buy_order(symbol, quantity, price):
    return create_add_order(symbol, BUY, quantity, price)

def create_sell_order(symbol, quantity, price):
    return create_add_order(symbol, SELL, quantity, price)

def connect_to_test():
    print("CONNECTING TO TEST EXCHANGE")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("test-exch-jiffy", 25000))
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
    print("->" + order, file=sys.stderr)
    print(order, file=EXCHANGE)

def get_message():
    s = EXCHANGE.readline().strip()
    print("<-" + s, file=sys.stderr)
    return json.loads(s)


