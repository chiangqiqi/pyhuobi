#!/usr/bin/env python

import logging

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
        try:
            self._acc_id = accounts['data'][0]['id']
        except:
            logging.warning("can not get accid")
            
    def _get_accounts(self):
        """
        :return:
        """
        path = "/v1/account/accounts"
        params = {}
        return self.auth.get(path, params)


    def send_order(self, amount, source, symbol, _type, price=None):
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
        period_values = ['1min', '5min', '15min', '30min','60min', '1day', '1mon', '1week', '1year']
        if period not in period_values:
            raise ValueError(f"Period should be in {period_values}")
        
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

    def get_orders(self, symbol, states='filled'):
        """获取当前委托历史委托
        states: pre-submitted 准备提交, submitted 已提交, partial-filled 部分成交,
                partial-canceled 部分成交撤销, filled 完全成交, canceled 已撤销
        """
        params = {
            'symbol': symbol,
            'states': states
        }

        url = '/v1/order/orders'
        return self.auth.get(url, params)

    def get_trades(self, symbol, _type=None):
        """获取当前交易， 历史交易
        """
        params = {
            'symbol': symbol,
            'type': _type
        }
        url = '/v1/order/matchresults'
        return self.auth.get(url, params)

    def get_markets(self):
        """get all symbols
        """
        url = '/market/tickers'
        return self.auth.get(url, {})
