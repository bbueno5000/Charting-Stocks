import datetime
import matplotlib
import matplotlib.dates as mpl_dates
import matplotlib.finance.candlestick as candlestick
import matplotlib.pyplot as pyplot
import matplotlib.ticker as mpl_ticker
import numpy
import pylab
import time

matplotlib.rcParams.update({'font.size': 9})

each_stock = 'EBAY', 'AAPL', 'TSLA'

def compute_macd(self, x, slow=26, fast=12):
        """
        Compute MACD using a fast and slow exponential moving average.

        Definitions:
            macd - moving average convergence/divergence
            ema - exponential moving average
            macd line = 12 ema - 26 ema
            signal line = 9 ema of macd line
            histogram = macd line - signal line

        Returns:
            len(x) arrays: value is emaslow, emafast, macd
        """
        ema_slow = self.exponential_moving_average(x, slow)
        ema_fast = self.exponential_moving_average(x, fast)
        return emaslow, emafast, emafast - emaslow

def exponential_moving_average(values, window):
    """
    Definitions:
        ema = exponential moving average
    """
    weights = np.exp(np.linspace(-1.0, 0.0, window))
    weights /= weights.sum()
    ema = np.convolve(values, weights, mode='full')[:len(values)]
    ema[:window] = ema[window]
    return ema

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
        ax2 - axis 2
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
        figure = pyplot.figure(facecolor='#07000D')
        # axis 1
        ax1 = pyplot.subplot2grid((5,4), (1,0), rowspan=4, colspan=4, axisbg='#07000D')
        candlestick(
            ax1, 
            candle_args[-sp:], 
            width=0.6, 
            colorup='#53C156', 
            colordown='#FF1717'
            )
        ax1.plot(
            date[-sp:], 
            av1[-sp:], 
            '#E1EDF9', 
            label=label_1, 
            linewidth=1.5
            )
        ax1.plot(
            date[-sp:], 
            av2[-sp:], 
            '#4EE6FD', 
            label=label_2, 
            linewidth=1.5
            )
        ax1.xaxis.set_major_locator(mpl_ticker, MaxNLocator(10))
        ax1.xaxis.set_major_formatter(mpl_dates.DateFormatter('%Y-%m-%d'))
        pyplot.gca().yaxis.set_major_locator(mpl_ticker.MaxNLocator(prune='upper'))
        ax1.grid(True, color='w')
        ax1.yaxis.label.set_color('w')
        ax1.spines['bottom'].set_color('#5998FF')
        ax1.spines['top'].set_color('#5998FF')
        ax1.spines['left'].set_color('#5998FF')
        ax1.spines['right'].set_color('#5998FF')
        ax1.tick_params(axis='x', colors='w')
        ax1.tick_params(axis='y', colors='w')
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
            axisbg='#07000D'
            )
        rsi = relative_strength_index(closep)
        rsi_color = '#1A8782'
        pos_color = '#386D13'
        neg_color = '#8F2020'
        ax0.plot(
            date[-sp:], 
            rsi[-sp:], 
            rsi_color, 
            linewidth=1.5
            )
        ax0.axhline(70, color=neg_color)
        ax0.axhline(30, color=pos_color)
        ax0.fill_between(
            date[-sp:],
            rsi[-sp:], 
            70, 
            where=(rsi[-sp:]>=70), 
            facecolor=neg_color, 
            edgecolor=neg_color
            )
        ax0.fill_between(
            date[-sp:], 
            rsi[-sp:], 
            30, 
            where=(rsi[-sp:]<=30), 
            facecolor=pos_color, 
            edgecolor=neg_color
            )
        ax0.spines['bottom'].set_color('#5998ff')
        ax0.spines['top'].set_color('#5998ff')
        ax0.spines['left'].set_color('#5998ff')
        ax0.spines['right'].set_color('#5998ff')
        ax0.text(0.015, 0.95, 'RSI (14)', va='top', color='w', transform=ax0.transAxes)
        ax0.tick_params(axis='x', colors='w')
        ax0.tick_params(axis='y', colors='w')
        ax0.set_yticks([30, 70])
        #pyplot.gca().yaxis.set_major_locator(mpl_ticker.MaxNLocator(prune='lower'))
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
        # axis 2
        ax2 = pyplot.subplot2grid(
            (6, 4), 
            (5, 0), 
            sharex=ax1, 
            rowspan=1, 
            colspan=4, 
            axisbg='#07000d'
            )
        fill_color = '#00ffe8'
        num_slow = 26
        num_fast = 12
        num_ema = 9
        ema_slow, ema_fast, macd = compute_macd(closep)
        ema9 = exponential_moving_average(macd, num_ema)
        ax2.plot(date[-sp:], macd[-sp:], color='#4EE6FD', lw=2)
        ax2.plot(date[-sp:], ema9[-sp:], cplor='#E1EDF9', lw=1)
        ax2.text(0.015, 0.95, 'MACD 12, 26, 9', va='top', color='w', transform=ax2.transAxes)
        ax2.fill_between(date[-sp:], macd[-sp:]-ema9[-sp:], 0, alpha=0.5, facecolor=fill_color, edgecolor=fill_color)
        ax2.spines['bottom'].set_color('#5998ff')
        ax2.spines['top'].set_color('#5998ff')
        ax2.spines['left'].set_color('#5998ff')
        ax2.spines['right'].set_color('#5998ff')
        ax2.tick_params(axis='x', colors='w')
        ax2.tick_params(axis='y', colors='w')
        #pyplot.ylabel('MACD', color='w')
        pyplot.gca().yaxis.set_major_locator(mpl_ticker.MaxNLocator(prune='upper'))
        ax2.yaxis.set_major_locator(mpl_ticker.MaxNLocator(nbins=5, prune='upper'))
        for label in ax2.xaxis.get_ticklabels():
            label.set_rotation(45)
        # super
        pyplot.suptitle(stock, color='w')
        pyplot.setp(ax0.get_xticklabels(), visible=False)
        pyplot.setp(ax1.get_xticklabels(), visible=False)
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
