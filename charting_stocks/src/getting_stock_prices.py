import datetime
import time
import urllib.request

stock_to_pull = 'AAPL', 'GOOG', 'MSFT', 'CMG', 'AMZN', 'EBAY', 'TSLA'

def pull_data(stock):
	try:
		print('currently pulling ', stock)
		print(str(datetime.datetime.fromtimestamp(time.time())).strftime('%Y-%m-%d %H:%M:%S'))
		url_to_visit = 'http://chartapi.finance.yahoo.com/instrument/1.0/' + stock + '/chartdata;type=quote;range=10d/csv'
		save_file_line = stock + '.txt' 
		try:
			read_existing_data = open(save_file_line, 'r').read()
			split_existing = read_existing_data.split('\n')
			most_recent_line = split_existing[-2]
			last_unix = most_recent_line.split(',')[0]
		except:
			last_unix = 0
		save_file = open(save_file_line, 'a')
		source_code = urllib.request.urlopen(url_to_visit).read()
		split_source = source_code.split('\n')
		for line in split_source:
			if 'values' not in line:
				split_line = line.split(',')
				if len(split_line) == 6:
					if int(split_line[0]) > int(last_unix):
						line_to_write = line + '\n'
						save_file.write(line_to_write)
		save_file.close()
		print('pulled', stock)
		print('sleeping...')
		print(str(datetime.datetime.fromtimestamp(time.time())).strftime('%Y-%m-%d %H:%M:%S'))
		time.sleep(10)
	except Exception as e:
		print('main loop', str(e))

if __name__ == '__main__':
	while true:
		for stock in stock_to_pull:
			pull_data(stock)
	time.sleep(18000)
