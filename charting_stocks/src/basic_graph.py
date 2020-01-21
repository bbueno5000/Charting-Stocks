import datetime
import matplotlib.pyplot as pyplot
import matplotlib.ticker as mpl_ticker
import matplotlib.dates as mpl_dates
import numpy
import time

each_stock = 'AAPL', 'TSLA'

def graph_data(stock):
    try:
        stock_file = stock + '.txt'
        date, closep, highp, lowp, openp, volume = numpy.loadtxt(
            stock_file, delimiter=',', unpack=true, converters={0: mpl_dates.strpdate2num('%Y%m%d')}
            )
        figure = pyplot.figure()
        axis1 = pyplot.subplot(1, 1, 1)
        axis1.plot(date, openp)
        axis1.plot(date, highp)
        axis1.plot(date, lowp)
        axis1.plot(date, closep)
        axis1.xaxis.set_major_locator(mpl_ticker, MaxNLocator(10))
        axis1.xaxis.set_major_formatter(mpl_dates.DateFormatter('%Y-%m-%d'))
        for label in axis1.xaxis.get_ticklabels():
            label.set_rotation(45)
        pyplot.show()
    except Exception as e:
        print('main loop', str(e))

if __name__ == '__main__':
	for stock in each_stock:
		pull_data(stock)
	time.sleep(500)