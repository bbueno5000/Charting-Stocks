﻿import datetime
import matplotlib
import matplotlib.dates as mpl_dates
from matplotlib.finance import candlestick
import matplotlib.pyplot as pyplot
import matplotlib.ticker as mpl_ticker
import numpy
import pylab
import time

matplotlib.rcParams.update({'font.size': 9})

each_stock = 'EBAY', 'AAPL', 'TSLA'

def graph_data(stock, mov_avg_1, mov_avg_2):
    """
    Parameters:
        stock
        mov_avg_1: moving average 1
        mov_avg_2: moving average 2
    
    Definitions:
        av1 - average 1
        av2 - average 2
        ax0 - axis 0
        ax1 - axis 1
        ax1vol - axis 1 volume
        rsi - relative strength index
        sp - starting point
        vol_min - volume minimum
    """
    try:
        stock_file = stock + '.txt'
        date, closep, highp, lowp, openp, volume = numpy.loadtxt(
            stock_file, 
            delimiter=',', 
            unpack=true, 
            converters={0: mpl_dates.strpdate2num('%Y%m%d')}
            )
        x = 0
        y = len(date)
        candle_args = []
        while x < y:
            append_line = date[x], openp[x], closep[x], highp[x], lowp[x], volume[x]
            candle_args.append(append_line)
            x += 1
        av1 = moving_average(closep, mov_avg_1)
        av2 = moving_average(closep, mov_avg_2)
        sp = len(date[mov_avg_2-1:])
        label_1 = str(mov_avg_1) + ' SMA'
        label_2 = str(mov_avg_2) + ' SMA'
        figure = pyplot.figure(facecolor='#07000d')
        # axis 1
        ax1 = pyplot.subplot2grid((5,4), (1,0), rowspan=4, colspan=4, axisbg='#07000d')
        candlestick(
            ax1, 
            candle_args[-sp:], 
            width=0.6, 
            colorup='#9eff15', 
            colordown='#f1717'
            )
        ax1.plot(
            date[-sp:], 
            av1[-sp:], 
            '#5998ff', 
            label=label_1, 
            linewidth=1.5
            )
        ax1.plot(
            date[-sp:], 
            av2[-sp:], 
            '#e1edf9', 
            label=label_2, 
            linewidth=1.5
            )
        ax1.xaxis.set_major_locator(mpl_ticker, MaxNLocator(10))
        ax1.xaxis.set_major_formatter(mpl_dates.DateFormatter('%Y-%m-%d'))
        ax1.grid(True, color='w')
        ax1.yaxis.label.set_color('w')
        ax1.spines['bottom'].set_color('#5998ff')
        ax1.spines['top'].set_color('#5998ff')
        ax1.spines['left'].set_color('#5998ff')
        ax1.spines['right'].set_color('#5998ff')
        ax1.tick_params(axis='x', colors='w')
        ax1.tick_params(axis='y', colors='w')
        for label in ax1.xaxis.get_ticklabels():
            label.set_rotation(45)
        pyplot.ylabel('Stock Price And Volume')
        ma_legend = pyplot.legend(fancybox=True, loc=9, ncol=2, prop={'size': 7})
        ma_legend.get_frame().set_alpha(0.4)
        text_ed = pylab.gca().get_legend().get_texts()
        pylab.setp(text_ed[0:5], color='w')
        # axis 0
        ax0 = pyplot.subplot2grid(
            (5,4), 
            (0,0), 
            sharex=ax1, 
            rowspan=1, 
            colspan=4, 
            axisbg='#07000d'
            )
        rsi = relative_strength_index(closep)
        rsi_color = '#00ffe8'
        ax0.plot(
            date[-sp:], 
            rsi[-sp:], 
            rsi_color, 
            linewidth=1.5
            )
        ax0.axhline(70, color=rsi_color)
        ax0.axhline(30, color=rsi_color)
        ax0.fill_between(
            date[-sp:],
            rsi[-sp:], 
            70, 
            where=(rsi[-sp:]>=70), 
            facecolor=rsi_color, 
            edgecolor=rsi_color
            )
        ax0.fill_between(
            date[-sp:], 
            rsi[-sp:], 
            30, 
            where=(rsi[-sp:]<=30), 
            facecolor=rsi_color, 
            edgecolor=rsi_color
            )
        ax0.spines['bottom'].set_color('#5998ff')
        ax0.spines['top'].set_color('#5998ff')
        ax0.spines['left'].set_color('#5998ff')
        ax0.spines['right'].set_color('#5998ff')
        ax0.tick_params(axis='x', colors='w')
        ax0.tick_params(axis='y', colors='w')
        ax0.set_yticks([30, 70])
        #pyplot.gca().yaxis.set_major_locator(mpl_ticker.MaxNLocator(prune='lower'))
        pyplot.ylabel('RSI')
        # axis 1 volume
        vol_min = 0
        ax1vol = ax1.twinx()
        ax1vol.fill_between(date[-sp:], vol_min, volume[-sp:], facecolor='#00ffe8', alpha=0.5)
        ax1vol.axes.yaxis.set_ticklabels([])
        ax1vol.grid(False)
        ax1vol.spines['bottom'].set_color('#5998ff')
        ax1vol.spines['top'].set_color('#5998ff')
        ax1vol.spines['left'].set_color('#5998ff')
        ax1vol.spines['right'].set_color('#5998ff')
        ax1vol.set_ylim(0, 2*volume.max())
        ax1vol.tick_params(axis='x', colors='w')
        ax1vol.tick_params(axis='y', colors='w')
        # super
        pyplot.suptitle(stock, color='w')
        pyplot.setp(ax0.get_xticklabels(), visible=False)
        pyplot.subplots_adjust(left=0.9, bottom=0.14, right=0.94, top=0.95, wspace=0.2, hspace=0)
        pyplot.show()
        figure.savefig('example.png', facecolor=figure.get_facecolor())
    except Exception as e:
        print('main loop', str(e))

def moving_average(values, window):
    weights = numpy.repeat(1.0, window) / window
    smas = numpy.convolve(values, weights, 'valid')
    return smas

def relative_strength_index(prices, n=14):
    """
    definitions:
        rs - relative strength
        rsi - relative strength index
    """
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed>=0].sum()/n
    down = -seed[seed<0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100.0 - 100.0 / (1.0 + rs)
    for i in range(n, len(prices)):
        delta = deltas[i-1]
        if delta > 0:
            up_value = delta
            down_value = 0.0
        else:
            up_value = 0.0
            down_value = -delta
        up = (up * (n-1) + up_value) / n
        down = (down * (n-1) + down_value) / n
        rs = up / down
        rsi[i] = 100.0 - 100.0 / (1.0+rs)
    return rsi

if __name__ == '__main__':
	for stock in each_stock:
		pull_data(stock, 20, 200)
	time.sleep(500)
