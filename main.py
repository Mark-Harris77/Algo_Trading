import os
import pandas as pd
import datetime
from strategy import indicate
debug = False
#TODO
#need a date handler or smth to allow same rows in different tables to have different dates
#finish trading method that sells all remaining stocks
#some kind of print report method which shows current money / stocks owned
#maybe move loop marked 1 into strategy
#IMPORTANT share price seems wrong

def get_file(filename):
    filename = os.path.join("data", filename)
    filename += ".csv"
    try:
        return pd.read_csv(filename)
    except:
        if debug: print("Error Opening File: " + filename)      

class stock:
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.owned = 0

    def get_data(self, date):
        if (self.data['Date'] == str(date)[:10]).any():
            index = self.data[self.data['Date'] == str(date)[:10]].index
            return self.data[:index[0]]
        else:
            return None
    
    def get_share_price(self, date):
        #return self.data.at[self.current_day, 'Adj Close']
        if (self.data['Date'] == str(date)[:10]).any():
            return float(self.data.loc[self.data['Date'] == str(date)[:10]]['Adj Close'])
        else:
            #look for previous days to sell from
            for i in range(30):
                date -= datetime.timedelta(days=1)
                if (self.data['Date'] == str(date)[:10]).any():
                    return float(self.data.loc[self.data['Date'] == str(date)[:10]]['Adj Close'])
        
        


class controller:
    def __init__(self, money, stocks_to_trade, start_date, end_date):
        self.money = money
        self.c_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        self.e_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        #setup the portfolio dictonary
        self.portfolio = {}
        for s in stocks_to_trade:
            self.portfolio[s] = stock(s, get_file(s))

    def isFinished(self):
        if self.c_date == self.e_date:
            return True
        else:
            return False

    def buy(self, name, shares=0):
        if name in self.portfolio:

            share_price = self.portfolio[name].get_share_price(self.c_date)
            if share_price is None:
                return False
            #when shares is 0 assume buy max possible
            if shares == 0:
                shares = self.money // share_price
                if shares == 0:
                    if debug: print('Not enough money to buy shares in ' + name)
                    return False
                else:
                    self.money -= shares * share_price
                    self.portfolio[name].owned += shares
                    return True

            else:
                if self.money < shares * share_price:
                    if debug: print('Not enough to complete transaction')
                    return False
                else:
                    self.money -= shares * share_price
                    self.portfolio[name].owned += shares
                    return True

        else:
            if debug: print(name + " couldnt be found in portfolio")
            return False
    
    def sell(self, name, shares=0):
        if name in self.portfolio:
            
            share_price = self.portfolio[name].get_share_price(self.c_date)
            if share_price is None:
                return False
            if self.portfolio[name].owned == 0:
                if debug: print('No shares in ' + name)
                return False
            #if shares = 0 then assume sell all
            if shares == 0:
                shares = self.portfolio[name].owned
                self.portfolio[name].owned = 0
                self.money += shares * share_price
                return True
            else:
                if self.portfolio[name].owned < shares:
                    if debug: print('Not enough shares in ' + name + 'owned')
                    return False
                else:
                    self.portfolio[name].owned -= shares
                    self.money += shares * share_price
                    return True

        else:
            if debug: print(name + " couldnt be found in portfolio")
            return False

    def increment_day(self):
        self.c_date += datetime.timedelta(days=1)

        






stocks = ['AAPL']
start_money = 1000

trade_controller = controller(start_money, stocks, "2000-12-01", "2020-01-01")
# trade_controller.portfolio['AAPL'].update_day()
# print(trade_controller.portfolio['AAPL'].get_data())

while not trade_controller.isFinished():
    #1
    for stock in trade_controller.portfolio.values():
        #print('Share Price', stock.get_share_price(trade_controller.c_date))
        data = stock.get_data(trade_controller.c_date)
        if data is not None:
            ind = indicate(data)
            if ind:
                #buy
                trade_controller.buy(stock.name)
            else:
                #sell
                trade_controller.sell(stock.name)
                
    trade_controller.increment_day()
    #print(trade_controller.c_date, trade_controller.money)

trade_controller.sell('AAPL')
print(trade_controller.money)