import datetime
import matplotlib
import matplotlib.dates as mpl_dates
from matplotlib.finance import candlestick
import matplotlib.pyplot as pyplot
import matplotlib.ticker as mpl_ticker
import numpy
import time

matplotlib.rcParams.update({'font.size': 9})

each_stock = 'AAPL', 'TSLA'

def graph_data(stock):
    try:
        stock_file = stock + '.txt'
        date, closep, highp, lowp, openp, volume = numpy.loadtxt(
            stock_file, delimiter=',', unpack=true, converters={0: mpl_dates.strpdate2num('%Y%m%d')}
            )
        x = 0
        y = len(date)
        candle_args = []
        while x < y:
            append_line = date[x], openp[x], closep[x], highp[x], lowp[x], volume[x]
            candle_args.append(append_line)
            x += 1
        figure = pyplot.figure()
        axis1 = pyplot.subplot2grid((5,4), (0,0), rowspan=4, colspan=4)
        candlestick(axis1, candle_args, width=1, colorup='g', colordown='r')
        pyplot.ylabel('Stock Price')
        axis1.grid(True)
        axis2 = pyplot.subplot2grid((5,4), (4,0), sharex=axis1, rowspan=1, colspan=4)
        axis2.bar(date, volume)
        axis2.axes.yaxis.set_ticklabels([])
        pyplot.ylabel('Volume')        
        axis2.grid(True)
        axis1.xaxis.set_major_locator(mpl_ticker, MaxNLocator(10))
        axis1.xaxis.set_major_formatter(mpl_dates.DateFormatter('%Y-%m-%d'))
        for label in axis1.xaxis.get_ticklabels():
            label.set_rotation(90)
        for label in axis2.xaxis.get_ticklabels():
            label.set_rotation(45)
        pyplot.xlabel('Date')
        pyplot.suptitle(stock + 'Stock Price')
        pyplot.setp(axis1.get_xticklabels(), visible=False)
        pyplot.subplots_adjust(left=0.9, bottom=0.18, right=0.94, top=0.94, wspace=0.2, hspace=0)
        pyplot.show()
        figure.savefig('example.png')
    except Exception as e:
        print('main loop', str(e))

if __name__ == '__main__':
	for stock in each_stock:
		pull_data(stock)
	time.sleep(500)
