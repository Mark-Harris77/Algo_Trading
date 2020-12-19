import os
import pandas as pd
from strategy import indicate

def get_file(filename):
    filename = os.path.join("data", filename)
    filename += ".csv"
    try:
        return pd.read_csv(filename)
    except:
        print("Error Opening File: " + filename)



f = input("Enter Stock name: \n")
d = get_file(f)

for i in range(30, len(d)):
    ind = indicate(d[:i])
    print(ind)