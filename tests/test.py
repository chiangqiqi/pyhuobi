"""Huobi api test
"""


from huobi.client import Huobi

from .config import * 

# pkey = "*"
# skey = "*"
huobi = Huobi(pkey, skey)


def test_balance():
    res = huobi.get_balance()

def test_depth():
    res = huobi.get_depth("ethbtc")
