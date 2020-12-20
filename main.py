import os
import pandas as pd
from strategy import indicate

#TODO
#need a date handler or smth to allow same rows in different tables to have different dates
#finish trading method that sells all remaining stocks
#some kind of print report method which shows current money / stocks owned


def get_file(filename):
    filename = os.path.join("data", filename)
    filename += ".csv"
    try:
        return pd.read_csv(filename)
    except:
        print("Error Opening File: " + filename)


class stock:

    current_day = 30

    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.owned = 0

    def get_data(self):
        return self.data[:self.current_day]
    
    def get_share_price(self):
        return self.data.at[self.current_day, 'Adj Close']

    @classmethod
    def update_day(cls):
        cls.current_day += 1

class controller:
    def __init__(self, money, stocks_to_trade):
        self.money = money

        #setup the portfolio dictonary
        self.portfolio = {}
        for s in stocks_to_trade:
            self.portfolio[s] = stock(s, get_file(s))

    def buy(self, name, shares=0):
        if name in self.portfolio:

            share_price = self.portfolio[name].get_share_price()

            #when shares is 0 assume buy max possible
            if shares == 0:
                shares = self.money // share_price
                if shares == 0:
                    print('Not enough money to buy shares in ' + name)
                    return False
                else:
                    self.money -= shares * share_price
                    self.portfolio[name].owned += shares
                    return True

            else:
                if self.money < shares * share_price:
                    print('Not enough to complete transaction')
                    return False
                else:
                    self.money -= shares * share_price
                    self.portfolio[name].owned += shares
                    return True

        else:
            print(name + " couldnt be found in portfolio")
            return False
    
    def sell(self, name, shares=0):
        if name in self.portfolio:
            
            share_price = self.portfolio[name].get_share_price()

            if self.portfolio[name].owned == 0:
                print('No shares in ' + name)
                return False
            #if shares = 0 then assume sell all
            if shares == 0:
                shares = self.portfolio[name].owned
                self.portfolio[name].owned = 0
                self.money += shares * share_price
                return True
            else:
                if self.portfolio[name].owned < shares:
                    print('Not enough shares in ' + name + 'owned')
                    return False
                else:
                    self.portfolio[name].owned -= shares
                    self.money += shares * share_price
                    return True

        else:
            print(name + " couldnt be found in portfolio")
            return False
        






stocks = ['AAPL']
start_money = 1000

trade_controller = controller(start_money, stocks)
trade_controller.portfolio['AAPL'].update_day()
print(trade_controller.portfolio['AAPL'].get_data())

for i in range(4500):
    for stock in trade_controller.portfolio.values():
        data = stock.get_data()
        ind = indicate(data)
        if ind:
            #buy
            trade_controller.buy(stock.name)
        else:
            #sell
            trade_controller.sell(stock.name)
    stock.update_day()
    print(stock.current_day, trade_controller.money)

trade_controller.sell('AAPL')
print(trade_controller.money)