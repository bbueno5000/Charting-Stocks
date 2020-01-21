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
        axis1 = pyplot.subplot(2, 1, 1)
        axis1.plot(date, openp)
        axis1.plot(date, highp)
        axis1.plot(date, lowp)
        axis1.plot(date, closep)
        pyplot.ylabel('Stock Price')
        axis1.grid(True)
        axis2 = pyplot.subplot(2, 1, 2, sharex=axis1)
        axis2.bar(date, volume)
        pyplot.ylabel('Volume')        
        axis2.grid(True)
        axis1.xaxis.set_major_locator(mpl_ticker, MaxNLocator(10))
        axis1.xaxis.set_major_formatter(mpl_dates.DateFormatter('%Y-%m-%d'))
        for label in axis1.xaxis.get_ticklabels():
            label.set_rotation(90)
        for label in axis2.xaxis.get_ticklabels():
            label.set_rotation(45)
        pyplot.subplots_adjust(left=0.1, bottom=0.19, right=0.93, top=0.95, wspace=0.2, hspace=0.07)
        pyplot.xlabel('Date')
        pyplot.suptitle(stock + 'Stock Price')
        pyplot.show()
    except Exception as e:
        print('main loop', str(e))

if __name__ == '__main__':
	for stock in each_stock:
		pull_data(stock)
	time.sleep(500)