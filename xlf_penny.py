import library
BOND_PRICE = 1000
BOND_ALLOWED = 100
SYMBOL = 'symbol'
BOOK = 'book'
TYPE = 'type'
BUY = 'buy'
OUT = 'out'
SELL ='sell'
FILL ='fill'
DIR = 'dir'
ACK = 'ack'
REJECT = 'reject'
ORDER_ID = 'order_id'

SYMBOL_PENNIED = library.XLF
MIN_SPREAD = 50

   
PENNY_SIZE = 1


class Order:
    def __init__(self):
        self.id = None
        self.price = None
        self.state_known = True
        self.size = None
    def cancel_if_needed(self):
        if self.id != None:
            library.send_cancel_order(self.id)
            self.state_known = False
    
    def kill(self):
        self.id = None
        self.price = None
        self.state_known = True
        self.size = None

buy_order = Order()
sell_order = Order()


def get_symbol_from_map_tuple(t):
    return t[0]

def is_it_my_order(msg):
    id = msg[ORDER_ID]
    tup = library.id_to_symbol_map[id]
    return get_symbol_from_map_tuple(tup) == SYMBOL_PENNIED

def on_start():
    pass

def print_orders():
    print("buy_order:")
    print(buy_order.id, buy_order.price, buy_order.state_known,
            buy_order.size)
    print("sell_order:")
    print(sell_order.id, sell_order.price, sell_order.state_known,
            sell_order.size)

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
    if msg[TYPE] == OUT:
        if is_it_my_order(msg):
            penny_valbz_handle_out(msg)

def penny_valbz_handle_book(buy, sell):
    try:
        if not do_we_know_state():
            return
        if not do_we_want_to_penny(buy, sell):
            if are_we_in():
                get_out()
                raise NameError("asdas")
        else:
            # we want to penny
            if not are_we_in():
                start_pennying(buy, sell)
            else:
                if is_our_pennying_reasonable(buy, sell, buy_order.price,
                        sell_order.price):
                    return
                else:
                    get_out()
    except:
        pass

def penny_valbz_handle_reject(msg):
    print ("Rejected because ", msg["error"])
    id = msg[ORDER_ID]
    print("valbz_reject")
    if id != buy_order.id and id != sell_order.id:
        raise Error("invalid id")
    if id == buy_order.id:
        buy_order.kill()
        if sell_order.id != None:
            sell_order.cancel_if_needed()
    if id == sell_order.id:
        sell_order.kill()
        if buy_order.id != None:
            buy_order.cancel_if_needed()
    pass

def penny_valbz_handle_ack(msg):
    id = msg[ORDER_ID]
    print("valbz_ack")
    if buy_order.id == id:
        buy_order.state_known = True
        return
    if sell_order.id == id:
        sell_order.state_known = True
        return
    print("Unrecognized ack")

def penny_valbz_handle_fill(msg):
    get_out()
    print("valbz_fill")
    pass

def penny_valbz_handle_out(msg):
    print("valbz_out")
    id = msg[ORDER_ID]
    if buy_order.id == id:
        buy_order.kill()
        return
    if sell_order.id == id:
        sell_order.kill()
        return
    pass
##################3
def do_we_want_to_penny(buy, sell):
    if len(buy) == 0 or len(sell) == 0:
        print("No market, no pennying")
        return False
    print("Spread: "+ str(sell[0][0] - buy[0][0]))
    return sell[0][0] - buy[0][0] > MIN_SPREAD

def is_our_pennying_reasonable(buy_book, sell_book, our_buy, our_sell):
    # we assume that pennying is reasonable, i.e. books are not empty
    top_buy = buy_book[0][0]
    top_sell = sell_book[0][0]
    return top_buy + 3 >= our_buy and our_buy >= top_buy and our_sell <= top_sell and top_sell - 3 <= our_sell 

def do_we_know_state():
    return buy_order.state_known and sell_order.state_known

def are_we_in():
    if not do_we_know_state():
        raise Error()
    if (buy_order.id == None) ^ (sell_order.id == None):
        get_out()
    return (buy_order.id != None and sell_order.id != None)

def get_out():
    buy_order.cancel_if_needed()
    sell_order.cancel_if_needed()

def start_pennying(buy, sell):
    buy_price = buy[0][0] + 1
    sell_price = sell[0][0] - 1
    if not do_we_know_state():
        raise Error("wtf")
    if are_we_in():
        raise Error("wtf")

    buy_order.price = buy_price
    sell_order.price = sell_price
    buy_order.size = PENNY_SIZE
    sell_order.size = PENNY_SIZE
    buy_order.state_known = False
    sell_order.state_known = False
    buy_order.id = library.send_buy_order(SYMBOL_PENNIED, buy_order.size,
            buy_order.price)
    sell_order.id = library.send_sell_order(SYMBOL_PENNIED, sell_order.size,
            sell_order.price)










