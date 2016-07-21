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

HELLO_MSG = json.dumps({"type" : "hello", "team" : "JIFFY"}) + "\n"

def create_add_order(idd, symbol, buy_or_sell, size, price):
    order = {"type": "add", "order_id": idd, "symbol": symbol, "dir": buy_or_sell, "price": price, "size": size}
    return json.dumps(order)

def create_buy_order(idd, symbol, quantity, price):
    return create_add_order(idd, symbol, BUY, quantity, price)

def create_sell_order(idd, symbol, quantity, price):
    return create_add_order(idd, symbol, SELL, quantity, price)

def connect_to_test():
    print("CONNECTING TO TEST EXCHANGE")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("test-exch-jiffy", 20000))
    global EXCHANGE
    EXCHANGE =  s.makefile('w+', 1)

def send_message(order):
    print(order, file=EXCHANGE)

def get_message():
    s = EXCHANGE.readline().strip()
    return json.loads(s)


