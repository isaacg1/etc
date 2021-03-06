import library
import position_tracking
from message_constants import *

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

def create_penny(symbol_pennied, min_spread, penny_size):

    COMPONENT_NAME = "PENNY "+ symbol_pennied
    SYMBOL_PENNIED = symbol_pennied
    MIN_SPREAD = min_spread
    PENNY_SIZE = penny_size

    buy_order = Order()
    sell_order = Order()


    def get_symbol_from_map_tuple(t):
        return t[0]

    def is_it_my_order(msg):
        id = msg[ORDER_ID]
        return library.id_to_component_map[id] == COMPONENT_NAME

    def penny(msg):
        if msg[TYPE] == BOOK and msg[SYMBOL] == SYMBOL_PENNIED:
            buy = msg[BUY]
            sell = msg[SELL]
            penny_handle_book(buy, sell)
        if msg[TYPE] == ACK:
            if is_it_my_order(msg):
                penny_handle_ack(msg)
        if msg[TYPE] == REJECT:
            if is_it_my_order(msg):
                penny_handle_reject(msg)
        if msg[TYPE] == FILL:
            if is_it_my_order(msg):
                penny_handle_fill(msg)
        if msg[TYPE] == OUT:
            if is_it_my_order(msg):
                penny_handle_out(msg)

    def penny_handle_book(buy, sell):
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
                    # if is_our_pennying_reasonable(buy, sell, buy_order.price,
                            # sell_order.price):
                        # return
                    # else:
                        get_out()
        except:
            pass

    def penny_handle_reject(msg):
        print ("Rejected because ", msg["error"], "  ", library.id_to_symbol_map[msg[ORDER_ID]])
        id = msg[ORDER_ID]
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

    def penny_handle_ack(msg):
        id = msg[ORDER_ID]
        if buy_order.id == id:
            buy_order.state_known = True
            return
        if sell_order.id == id:
            sell_order.state_known = True
            return
        print("Unrecognized ack")

    def penny_handle_fill(msg):
        get_out()

    def penny_handle_out(msg):
        id = msg[ORDER_ID]
        if buy_order.id == id:
            buy_order.kill()
            return
        if sell_order.id == id:
            sell_order.kill()
            return
        pass

    def do_we_want_to_penny(buy, sell):
        if len(buy) == 0 or len(sell) == 0:
            return False
        return sell[0][0] - buy[0][0] > MIN_SPREAD

    # def is_our_pennying_reasonable(buy_book, sell_book, our_buy, our_sell):
        # top_buy = buy_book[0][0]
        # top_sell = sell_book[0][0]
        # return top_buy + 3 >= our_buy and our_buy >= top_buy and our_sell <= top_sell and top_sell - 3 <= our_sell 

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
        shift = position_tracking.sym_to_pos[SYMBOL_PENNIED] / 20
        shift = 0
        buy_price = buy[0][0] + 1 - shift
        sell_price = sell[0][0] - 1 - shift
        if not do_we_know_state():
            raise NameError("wtf1")
        if are_we_in():
            raise NameError("wtf2")

        buy_order.price = buy_price
        sell_order.price = sell_price
        buy_order.size = PENNY_SIZE
        sell_order.size = PENNY_SIZE
        buy_order.state_known = False
        sell_order.state_known = False
        buy_order.id = library.send_buy_order(SYMBOL_PENNIED, buy_order.size,
                buy_order.price, COMPONENT_NAME)
        sell_order.id = library.send_sell_order(SYMBOL_PENNIED, sell_order.size,
                sell_order.price, COMPONENT_NAME)
    return penny
