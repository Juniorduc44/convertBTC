__version__="1.0.0"
from blockchain import exchangerates as ex

#Bitcoin Price Tracker
ticker = ex.get_ticker()
for k in ticker:
    if k == "USD":
        btcPrice = (ticker[k].p15min)

N = float(input('Enter the dollar amount you would like to convert into Bitcoin: '))
a = N / btcPrice
print("{:.8f}".format(a))