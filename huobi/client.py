#!/usr/bin/env python

from .utils import Auth

'''
Market data API
'''

class Huobi:
    def __init__(self, pkey, skey):
        """
        params:
        pkey: publice key,
        skey: secret key
        """
        # self._pkey = pkey
        # self._skey = skey
        self.auth = Auth(pkey, skey)
        accounts = self._get_accounts()
        self._acc_id = accounts['data'][0]['id']

    def _get_accounts(self):
        """
        :return: 
        """
        path = "/v1/account/accounts"
        params = {}
        return self.auth.get(path, params)


    def send_order(self, amount, source, symbol, _type, price=0):
        """
        :param amount:
        :param source: 如果使用借贷资产交易，请在下单接口,请求参数source中填写'margin-api'
        :param symbol:
        :param _type: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
        :param price:
        :return:
        """
        params = {"account-id": self._acc_id,
                  "amount": amount,
                  "symbol": symbol,
                  "type": _type,
                  "source": source}
        if price:
            params["price"] = price

        url = '/v1/order/orders/place'
        return self.auth.post(url, params)

    def get_balance(self):
        """
        :param acct_id
        :return:
        """
        url = "/v1/account/accounts/{0}/balance".format(self._acc_id)
        params = {"account-id": self._acc_id}
        return self.auth.get(url, params)


    def get_kline(self, symbol, period, size=150):
        """
        获取 kline
        :param symbol
        :param period: 可选值：{1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year }
        :param size: 可选值： [1,2000]
        :return:
        """
        params = {'symbol': symbol,
                  'period': period,
                  'size': size}

        url = '/market/history/kline'
        return self.auth.get(url, params)


    def get_depth(self, symbol, type='step0'):
        """
         获取marketdepth
        : param symbol
        :param type: 可选值：{ percent10, step0, step1, step2, step3, step4, step5 }
        :return:
        """
        params = {'symbol': symbol,
                  'type': type}

        url = '/market/depth'
        return self.auth.get(url, params)
