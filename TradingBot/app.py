import json, config
from flask import Flask, request, render_template
from binance.client import Client
from binance.enums import *

app = Flask(__name__)

client = Client(config.API_KEY, config.API_SECRET, tld='us')

def buy_order(side, quantity, symbol):
    if side == "BUY":   
        try:
            buy_order = client.order_market_buy(
                symbol=symbol,
                quantity=quantity)
            
            print(buy_order)

        except Exception as e:
            print("an exception occured - {}".format(e))
            return False
    else:
        pass

    return buy_order

def sell_order(side, quantity, symbol, price, stopPrice, stopLimitPrice):
    if side == "BUY":   
        try:  
            sell_order = client.order_oco_sell(
                symbol= symbol,                                            
                quantity= quantity,                                            
                price= price,                                            
                stopPrice= stopPrice,
                stopLimitPrice= stopLimitPrice,
                stopLimitTimeInForce = "GTC")
            
            print(sell_order)

        except Exception as e:
            print("an exception occured - {}".format(e))
            return False
    else:
        pass

    return sell_order


@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = json.loads(request.data)

    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        return {
            "code": "error",
            "message": "Nice try, invalid passphrase"
        }

    else:
        side = data['strategy']['order_action'].upper()
        quantity = data['strategy']['position_size']
        symbol = data['ticker']
        price = round(data['profit'], 2)
        stopPrice = round(data['stoploss'], 2)
        stopLimitPrice = round((1.005 * stopPrice))

    buy_order_response = buy_order(side=side, quantity=quantity, symbol=symbol)
    sell_order_response = sell_order(side=side, quantity=quantity, symbol=symbol, price=price, stopPrice=stopPrice, stopLimitPrice=stopLimitPrice)

    if buy_order_response:
        return {
            "code": "buy success"
        }

    if sell_order_response:
        return {
            "code": "sell success"
        }

    if buy_order_response and sell_order_response:
        return {
            "code": "success",
            "message": "order executed"
        }
    else:
        print("order failed")

        return {
            "code": "error",
            "message": "code failed"
        }