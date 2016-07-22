import library
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

def create_scale(symbol_scaled, scale_margin):

    COMPONENT_NAME = "SCALE " + symbol_svaled
    SYMBOL_SCALED = symbol_scaled
    SCALE_MARGIN = scale_margin
    SCALE_SIZE = scale_size

    buy_order = Order()
    sell_order = Order()


    def get_symbol_from_map_tuple(t):
        return t[0]

    def is_it_my_order(msg):
        id = msg[ORDER_ID]
        tup = library.id_to_symbol_map[id]
        return get_symbol_from_map_tuple(tup) == SYMBOL_SCALED

    def scale(msg):
        if msg[TYPE] == BOOK and msg[SYMBOL] == SYMBOL_SCALED:
            buy = msg[BUY]
            sell = msg[SELL]
            scale_handle_book(buy, sell)
        if msg[TYPE] == ACK:
            if is_it_my_order(msg):
                scale_handle_ack(msg)
        if msg[TYPE] == REJECT:
            if is_it_my_order(msg):
                scale_handle_reject(msg)
        if msg[TYPE] == FILL:
            if is_it_my_order(msg):
                scale_handle_fill(msg)
        if msg[TYPE] == OUT:
            if is_it_my_order(msg):
                scale_handle_out(msg)

    def scale_handle_book(buy, sell):
        try:
            if not do_we_know_state():
                return
            if not do_we_want_to_scale(buy, sell):
                if are_we_in():
                    get_out()
                    raise NameError("asdas")
            else:
                # we want to scale
                if not are_we_in():
                    start_scaleing(buy, sell)
                else:
                    # if is_our_scaleing_reasonable(buy, sell, buy_order.price,
                            # sell_order.price):
                        # return
                    # else:
                        get_out()
        except:
            pass

    def scale_handle_reject(msg):
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

    def scale_handle_ack(msg):
        id = msg[ORDER_ID]
        if buy_order.id == id:
            buy_order.state_known = True
            return
        if sell_order.id == id:
            sell_order.state_known = True
            return
        print("Unrecognized ack")

    def scale_handle_fill(msg):
        get_out()

    def scale_handle_out(msg):
        id = msg[ORDER_ID]
        if buy_order.id == id:
            buy_order.kill()
            return
        if sell_order.id == id:
            sell_order.kill()
            return
        pass

    def do_we_want_to_scale(buy, sell):
        if len(buy) == 0 or len(sell) == 0:
            return False
        return True

    # def is_our_scaleing_reasonable(buy_book, sell_book, our_buy, our_sell):
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

    def start_scaleing(buy, sell):
        CAP = 100 - 10
        fair = (buy[0][0] + sell[0][0]) / 2
        buy_price = fair + SCALE_MARGIN
        sell_price = fair - SCALE_MARGIN
        if not do_we_know_state():
            raise NameError("wtf1")
        if are_we_in():
            raise NameError("wtf2")

        buy_order.price = buy_price
        sell_order.price = sell_price
        current_bid_size = sym_to_bid_size[SYMBOL_SCALED]
        current_offer_size = sym_to_offer_size[SYMBOL_SCALED]
        buy_order.size = CAP - current_bid_size
        sell_order.size = CAP - current_offer_size
        buy_order.state_known = False
        sell_order.state_known = False
        buy_order.id = library.send_buy_order(SYMBOL_SCALED, buy_order.size,
                buy_order.price, COMPONENT_NAME)
        sell_order.id = library.send_sell_order(SYMBOL_SCALED, sell_order.size,
                sell_order.price, COMPONENT_NAME)
    return scale
