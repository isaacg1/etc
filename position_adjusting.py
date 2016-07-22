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

def create_position_adjusting(symbol_to_watch, max_spread, min_abs_position):

    COMPONENT_NAME = "GET RID OF POSITION IN "+ symbol_to_watch
    SYMBOL_TO_WATCH = symbol_to_watch
    MAX_SPREAD = max_spread
    ORDER_SIZE = 1
    MIN_ABS_POSITION = min_abs_position

    the_order = Order()

    def get_symbol_from_map_tuple(t):
        return t[0]

    def is_it_my_order(msg):
        id = msg[ORDER_ID]
        return library.id_to_component_map[id] == COMPONENT_NAME

    def strategy(msg):
        if msg[TYPE] == BOOK and msg[SYMBOL] == SYMBOL_TO_WATCH:
            buy = msg[BUY]
            sell = msg[SELL]
            handle_book(buy, sell)
        if msg[TYPE] == ACK:
            if is_it_my_order(msg):
                handle_ack(msg)
        if msg[TYPE] == REJECT:
            if is_it_my_order(msg):
                handle_reject(msg)
        if msg[TYPE] == FILL:
            if is_it_my_order(msg):
                handle_fill(msg)
        if msg[TYPE] == OUT:
            if is_it_my_order(msg):
                handle_out(msg)

    def handle_book(buy, sell):
        if not do_we_know_state():
            return
        if not do_we_want_to_adjust(buy, sell):
            if are_we_in():
                get_out()
        else:
            if not are_we_in():
                print ("we adjust2")
                adjust(buy, sell)
            else:
                print ("we're in so we back off and try again")
                get_out()

    def handle_reject(msg):
        print ("Rejected because ", msg["error"], "  ", library.id_to_symbol_map[msg[ORDER_ID]])
        id = msg[ORDER_ID]
        if id != the_order.id:
            raise Error("invalid id")
        if id == the_order.id:
            the_order.kill()

    def handle_ack(msg):
        id = msg[ORDER_ID]
        if the_order.id == id:
            the_order.state_known = True
            return
        print("Unrecognized ack ", COMPONENT_NAME)

    def handle_fill(msg):
        print ("We get out")
        get_out()

    def handle_out(msg):
        id = msg[ORDER_ID]
        if the_order.id == id:
            the_order.kill()

    def do_we_want_to_adjust(buy, sell):
        if len(buy) == 0 or len(sell) == 0:
            return False
        if abs(get_position(SYMBOL_TO_WATCH)) < MIN_ABS_POSITION:
            return False
        return sell[0][0] - buy[0][0] <= MAX_SPREAD

    def do_we_know_state():
        return the_order.state_known

    def are_we_in():
        if not do_we_know_state():
            raise Error()
        return the_order.id != None

    def get_out():
        the_order.cancel_if_needed()

    def get_position(smbl):
        return position_tracking.sym_to_pos[smbl]

    def adjust (buy, sell):
        print("sfasf")
        position = get_position(SYMBOL_TO_WATCH)
        sell_price = sell[0][0]
        buy_price = buy[0][0]
        print ("we adjust2", position, buy_price, sell_price)

        if not do_we_know_state():
            raise NameError("wtf1")
        if are_we_in():
            raise NameError("wtf2")

        if position > 0:    
            # we want to sell
            the_order.price = buy_price
            the_order.size = ORDER_SIZE
            the_order.state_known = False
            print("We sell for ", the_order.price)
            the_order.id = library.send_sell_order(SYMBOL_TO_WATCH, the_order.size,
                    the_order.price, COMPONENT_NAME)
        else:
            the_order.price = sell_price
            the_order.size = ORDER_SIZE
            the_order.state_known = False
            print("We buy for ", the_order.price)
            the_order.id = library.send_buy_order(SYMBOL_TO_WATCH, the_order.size,
                    the_order.price, COMPONENT_NAME)
            
    return strategy
