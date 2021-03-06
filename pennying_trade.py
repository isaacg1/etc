import library
from penny import create_penny

LOW_BETA_SPREAD = 20
NORMAL_BETA_SPREAD = 25
HIGH_BETA_SPREAD = 35
LIQUID_SPREAD = 20

ETF_SIZE = 3

etf_pennies = [ create_penny(library.XLY, HIGH_BETA_SPREAD, ETF_SIZE),
                create_penny(library.XLP, NORMAL_BETA_SPREAD, ETF_SIZE),
                create_penny(library.XLU, LOW_BETA_SPREAD, ETF_SIZE),
                create_penny(library.RSP, 50, ETF_SIZE)
                ]

STOCK_SIZE = 3
stock_pennies = [create_penny(library.AMZN, LIQUID_SPREAD, STOCK_SIZE),
                 create_penny(library.HD, HIGH_BETA_SPREAD, STOCK_SIZE),
                 create_penny(library.DIS, HIGH_BETA_SPREAD, STOCK_SIZE),
                 create_penny(library.PG, LIQUID_SPREAD, STOCK_SIZE),
                 create_penny(library.KO, NORMAL_BETA_SPREAD, STOCK_SIZE),
                 create_penny(library.PM, NORMAL_BETA_SPREAD, STOCK_SIZE),
                 create_penny(library.NEE, LIQUID_SPREAD, STOCK_SIZE),
                 create_penny(library.DUK, LOW_BETA_SPREAD, STOCK_SIZE),
                 create_penny(library.SO, LOW_BETA_SPREAD, STOCK_SIZE)]



