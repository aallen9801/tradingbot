# Overview
Presented is an automated trading bot I built in python using Flask and the Binance.US API. Also included is the custom trading algorithm I wrote myself using TradingView's PineScript. Enjoy!

# Part 1: The Trading Algorithm

In order to write and test the algorithm that the bot would use to know when to buy and sell, I use the platform TradingView. TradingView has their own coding language, Pine Script, to write these algorithms. The algorithm that I wrote uses two technical indicators: the Choppiness Index and Fibonacci Retracement. Choppiness Index measures the potential volatility of a crypto’s price. Fibonacci Retracement helps us identify support and resistance levels. The algorithm generated a “buy signal” based on 4 conditions. The first 3 conditions are from the Fibonacci Retracement indicator: 
The 1.0 Fibonacci Retracement level’s price is greater than the 0 level’s price. 
The 1.618 level’s price is above the 1.0 level’s price.
There was a price cross above the 1 level’s price.
This is what that part of code looked like in the script.

All the variables in the if statement are values from the Fibonacci Retracement indicator’s code. 
The fourth and final “buy signal” is from the Choppiness Index. It was to buy if the Choppiness Index was at a value of 54.5 or higher. Having this value or higher indicates high amount of potential swing in price.


The code to put these together and generate the buy signal looks for the ci_buy variable to be true and the fib_buy variable to also be true.

The next part I set up is the “sell signal”. This is programmed to sell when whichever of two conditions happens first. Either the cryptos price will cross under the 0 Fib. Retr. Level or it will sell when the price crosses above the 1.618 level.


The 0 level represents the stop loss price in the order to be created, and the 1.618 level represents the profit price in the order. In my case, I wanted to sell whenever one of those two price points are hit.

The first blue arrow indicates the price at which the buy signal is generated, and the second purple arrow indicates the price at which the sell signal is generated. These buy and sell signals trigger alerts in TradingView, and these alerts contain messages with information on what crypto to buy, when to buy it, and when to sell it. The format of these alerts use placeholders, which get filled in with values from the chart once the alert triggers.

The alert is formatted in JSON so that our python application will be able to extract the relevant information in order to create orders.

It is important to note that only the alert generated from the “buy” signal are used when creating both the buy and sell order in BinanceUS. This is because there are still bugs with the sell signal in the Pine Script algorithm, but everything can be accomplished solely from the buy signal. These buy alerts are sent straight from TradingView to my trading bot application that is hosted in the cloud. This is accomplished via a webhook url, which sends the contents of the alert message to my application. I use Heroku to host my application in the cloud. This is important because I wanted my bot to be running 24/7, so it would always be ready to place orders. Additionally, I would not need to have a local server running on my computer at all times and worry about my computer being charged, connected to the internet, etc.


# Part 2: The Trading Bot
I built this application using Flask, which is a framework for writing web applications in Python. There are two main functions, a buy order function and a sell order function. These functions use the Binance API, specifically their market buy order function and their OCO sell order function. The market order function will buy a certain amount of crypto at the current market price when the alert triggered. The OCO sell order will create two separate orders at once: the stop loss order and the take profit order. Whichever of these two order fills first will execute, and the other order, which is preferably the stop loss order will be cancelled because we would have already sold our crypto for profit.

The basic app home screen is nothing fancy, but the “/webhook” route in the webhook url brings the message to the trading bot. We post the alert message to that url, and the following code parses the messages for relevant information such as quantity to buy or sell, the ticker symbol, and the specific prices.

The code only runs if a passphrase that you create in your alert patches a passphrase that you create an import into your application from another file that is attached. That file contains your passphrase, your API public key, and your API secret key that you receive from BinanceUS. These keys are what connect the python application to your account in Binance. Therefore, if the passphrase from the TradingView alert does not match the passphrase that you set up previously, the order will not execute. This is obviously important in terms of security.

