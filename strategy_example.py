import numpy as np
def indicate(stock_data):
    SMA30 = stock_data.tail(30)['Adj Close'].mean()
    SMA100 = stock_data.tail(100)['Adj Close'].mean()
    if SMA30 > SMA100:
        return True
    else:
        return False
