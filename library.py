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

def create_add_order(idd, symbol, buy_or_sell, size, price):
    order = {"type": "add", "order_id": idd, "symbol": symbol, "dir": buy_or_sell, "price": price, "size": size}
    return json.dumps(order)

def create_buy_order(idd, symbol, quantity, price):
    return create_add_order(idd, symbol, BUY, quantity, price)

def create_sell_order(idd, symbol, quantity, price):
    return create_add_order(idd, symbol, SELL, quantity, price)

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("test-exch-jiffy", 20000))
    return s.makefile('w+', 1)

def send_order(order, exchange):
    print(order, file=exchange)
    response = exchange.readline().strip()
    print(response)

def main():
    exchange = connect()
    print("HELLO JIFFY", file=exchange)
    hello_from_exchange = exchange.readline().strip()
    print("The exchange replied:", hello_from_exchange, file=sys.stderr)
    send_order(create_buy_order(1, BOND, 1, 999), exchange)

if __name__ == "__main__":
    main()




