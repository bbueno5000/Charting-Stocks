import datetime
import matplotlib
import matplotlib.dates as mpl_dates
from matplotlib.finance import candlestick
import matplotlib.pyplot as pyplot
import matplotlib.ticker as mpl_ticker
import numpy
import time

matplotlib.rcParams.update({'font.size': 9})

each_stock = 'EBAY', 'AAPL', 'TSLA'

def graph_data(stock, moving_average_1, moving_average_2):
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
        average_1 = moving_average(closep, moving_average_1)
        average_2 = moving_average(closep, moving_average_2)
        starting_point = len(date[moving_average_2-1:])
        label_1 = str(moving_average_1) + ' SMA'
        label_2 = str(moving_average_2) + ' SMA'
        figure = pyplot.figure(facecolor='#07000d')
        # axis 0
        axis_0 = pyplot.subplot2grid((5,4), (0,0), rowspan=1, colspan=4, axisbg='#07000d')
        axis_0.spines['bottom'].set_color('#5998ff')
        axis_0.spines['top'].set_color('#5998ff')
        axis_0.spines['left'].set_color('#5998ff')
        axis_0.spines['right'].set_color('#5998ff')
        axis_0.tick_params(axis='x', colors='w')
        axis_0.tick_params(axis='y', colors='w')
        pyplot.gca().yaxis.set_major_locator(mpl_ticker.MaxNLocator(prune='lower'))
        pyplot.ylabel('RSI')
        # axis 1
        axis_1 = pyplot.subplot2grid((5,4), (1,0), rowspan=4, colspan=4, axisbg='#07000d')
        candlestick(
            axis_1, 
            candle_args[-starting_point:], 
            width=1, 
            colorup='#9eff15', 
            colordown='#f1717'
            )
        axis_1.plot(date[-starting_point:], average_1[-starting_point:], '#5998ff', label=label_1, linewidth=1.5)
        axis_1.plot(date[-starting_point:], average_2[-starting_point:], '#e1edf9', label=label_2, linewidth=1.5)
        axis_1.xaxis.set_major_locator(mpl_ticker, MaxNLocator(10))
        axis_1.xaxis.set_major_formatter(mpl_dates.DateFormatter('%Y-%m-%d'))
        axis_1.grid(True, color='w')
        axis_1.yaxis.label.set_color('w')
        axis_1.spines['bottom'].set_color('#5998ff')
        axis_1.spines['top'].set_color('#5998ff')
        axis_1.spines['left'].set_color('#5998ff')
        axis_1.spines['right'].set_color('#5998ff')
        axis_1.tick_params(axis='x', colors='w')
        axis_1.tick_params(axis='y', colors='w')
        for label in axis_1.xaxis.get_ticklabels():
            label.set_rotation(45)
        pyplot.ylabel('Stock Price')
        pyplot.legend(loc=3, fancybox=True, prop={'size': 7})
        # axis 1 volume
        volume_min = 0
        axis_1_volume = axis_1.twinx()
        axis_1_volume.fill_between(date, volume_min, volume, facecolor='#00ffe8', alpha=0.5)
        axis_1_volume.axes.yaxis.set_ticklabels([])
        axis_1_volume.grid(False)
        axis_1_volume.spines['bottom'].set_color('#5998ff')
        axis_1_volume.spines['top'].set_color('#5998ff')
        axis_1_volume.spines['left'].set_color('#5998ff')
        axis_1_volume.spines['right'].set_color('#5998ff')
        axis_1_volume.set_ylim(0, 2*volume.max())
        axis_1_volume.tick_params(axis='x', colors='w')
        axis_1_volume.tick_params(axis='y', colors='w')
        # super
        pyplot.suptitle(stock, color='w')
        pyplot.setp(axis_0.get_xticklabels(), visible=False)
        pyplot.subplots_adjust(left=0.9, bottom=0.14, right=0.94, top=0.95, wspace=0.2, hspace=0)
        pyplot.show()
        figure.savefig('example.png', facecolor=figure.get_facecolor())
    except Exception as e:
        print('main loop', str(e))

def moving_average(values, window):
    weights = numpy.repeat(1.0, window) / window
    smas = numpy.convolve(values, weights, 'valid')
    return smas

if __name__ == '__main__':
	for stock in each_stock:
		pull_data(stock, 12, 26)
	time.sleep(500)
