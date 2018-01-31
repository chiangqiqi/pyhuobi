# Huobi API

python3 version

## Overview

`huobi` 自己有一个简单的 python 客户端，不过比较难用，key 是写死在 `.py` 文件中，而且是 `py2`

这里做的工作是简单的做了一下封装。

## Example 

```python
from huobi.client import Huobi

client = Huobi(your_api_key, your_secret_key)

# 获取 balance
client.balance('eth')

# 获取 depth 
client.depth('ethusdt')

```

## Others 

PR is welcomed

and if this helps you, feel free to send me some tips:

ETH: 
LTC: 
