import time
import urllib.request

stock_to_pull = 'AAPL', 'GOOG', 'MSFT', 'CMG', 'AMZN', 'EBAY', 'TSLA'

def pull_data(stock):
    try:
        file_line = stock + '.txt'
        url_to_visit = 'http://chartapi.finance.yahoo.com/instrument/1.0/' + stock + '/chartdata;type=quote;range=1y/csv'
        source_code = urllib.request.urlopen(url_to_visit).read()
        split_source = source_code.split('\n')
        for line in split_source:
            split_line = line.split(',')
            if len(split_line) == 6:
                if 'values' not in line:
                    save_file = open(file_line, 'a')
                    line_to_write = line + '\n'
                    save_file.write(line_to_write)
        print('pulled', stock)
        print('sleeping...')
        time.sleep(1)
    except Exception as e:
        print('main loop', str(e))

if __name__ == '__main__':
    for stock in stock_to_pull:
        pull_data(stock)
