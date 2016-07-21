strategies = [ bond_trade ]


def run_strategies():
    for strategy in strategies:
        message = strategy()
