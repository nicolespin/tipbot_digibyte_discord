import requests
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
#from flask_jsonrpc.proxy import ServiceProxy

rpc_username = 'yourusername'
rpc_password = 'yourpassword'
rpc_ip = '127.0.0.1'
rpc_port = 14022


#Make rpc connection with DGB core
def ServiceProxy():
    return AuthServiceProxy('http://%s:%s@%s:%i'%(rpc_username, rpc_password, rpc_ip, rpc_port))

rpc_connection = ServiceProxy()


def validateAddress(address):
    rpc_connection = ServiceProxy()
    validate = rpc_connection.validateaddress(address)
    return validate['isvalid']

def getAddress(account):
    rpc_connection = ServiceProxy()
    account = rpc_connection.getaccountaddress(account)
    print(account)

    print(account)
    return account

def getBalance(account,minconf=1):
    rpc_connection = ServiceProxy()
    try:
        balance = rpc_connection.getbalance(account,minconf)
    except ValueError:
        balance = -1
    return balance

def withdraw(account,destination,amount):
    if amount > getBalance(account) or amount <= 0:
        raise ValueError("Invalid amount.")
    else:
        rpc_connection = ServiceProxy()
        return rpc_connection.sendfrom(account,destination,amount)

def tip(account,destination,amount):
    if amount > getBalance(account) or amount <= 0:
        raise ValueError("Invalid amount.")
    else:
        rpc_connection = ServiceProxy()
        rpc_connection.move(account,destination,amount)

def rain(account,amount):
    if amount > getBalance(account) or amount <= 0:
        raise ValueError("Invalid amount.")
    else:
        rpc_connection = ServiceProxy()
        accounts = rpc_connection.listaccounts()
        amount = 0
        eachTip = amount / len(accounts)
        for ac in accounts:
            tip(account,ac,eachTip)
        return eachTip

#API commands

def getPrice():
    api = requests.get('https://api.coinmarketcap.com/v1/ticker/digibyte/')
    r = api.json()[0]
    price = float(r['price_usd'])
    price_btc = float(r['price_btc'])

    return price, price_btc, r

def getPriceMSG():

    price, price_btc, r = getPrice()

    msg = "1 DGB = %9.8lf BTC (%9.8lf USD)\nMarket Cap. = %12.2lf USD (Rank: %d)\nChange in USD: %4.2lf pt. (1H), %4.2lf pt. (24H), %4.2lf pt. (7D)" % \
            (float(r['price_btc']), float(r['price_usd']), float(r['market_cap_usd']), int(r['rank']),\
            float(r['percent_change_1h']), float(r['percent_change_24h']), float(r['percent_change_1h']))

    return msg
