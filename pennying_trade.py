import library
from penny import create_penny

ETF_SPREAD = 20
STOCK_SPREAD = 20

ETF_SIZE = 10

etf_pennies = [ create_penny(library.XLY, ETF_SPREAD, ETF_SIZE),
                create_penny(library.XLP, ETF_SPREAD, ETF_SIZE),
                create_penny(library.XLU, ETF_SPREAD, ETF_SIZE),
                create_penny(library.RSP, ETF_SPREAD, ETF_SIZE)
                ]

STOCK_SIZE = 10
stock_pennies = [create_penny(library.AMZN, STOCK_SPREAD, STOCK_SIZE),
                 create_penny(library.HD, STOCK_SPREAD, STOCK_SIZE),
                 create_penny(library.DIS, STOCK_SPREAD, STOCK_SIZE),
                 create_penny(library.PG, STOCK_SPREAD, STOCK_SIZE),
                 create_penny(library.KO, STOCK_SPREAD, STOCK_SIZE),
                 create_penny(library.PM, STOCK_SPREAD, STOCK_SIZE),
                 create_penny(library.NEE, STOCK_SPREAD, STOCK_SIZE),
                 create_penny(library.DUK, STOCK_SPREAD, STOCK_SIZE),
                 create_penny(library.SO, STOCK_SPREAD, STOCK_SIZE)]



