import sys, os
import time
import datetime
import requests
import pandas as pd

def main(start_date, end_date, fpath):
	'''
	Parameters
	----------
	start_date : string,
		Should be in the format 'YYYYMMDD'
	end_date : string,
		Should be in the format 'YYYYMMDD'
	'''
	apiKey = 'XXXXXXXXXXXX'
	base_url = 'http://api.wunderground.com/api/{}/history_{}/q/KNYC.json'

	# -- get start and end dates
	sdate = pd.to_datetime(start_date)
	edate = pd.to_datetime(end_date)

	# -- for each day
	for i in range((edate - sdate).days):
		# -- build query
		query = base_url.format(apiKey, sdate.strftime('%Y%m%d'))
		print 'Weatherbot: fetching {}'.format(query)
    		
		# -- make request to WU API
		r = requests.get(query)
	
		# -- convert to dataframe		
		df = pd.DataFrame(r.json()['history']['observations'])

		df['date'] = df['date'].map(lambda x: x['pretty'])
		
		# -- check if the file already exists
		file_exists = os.path.isfile(fpath)
		with open(fpath,"a") as f:
			# -- create new file with header if necessary
			if not file_exists:
				df.to_csv(f, header=True, index=False)

			# -- append to exisiting file
			df.to_csv(f, header=False, index=False)
		
		# -- increment the start date by one day
		sdate += datetime.timedelta(days=1)
		
		# -- Weather Underground API accepts only 10 calls per minute
		time.sleep(10)
		
	print "Finished!"

if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2], sys.argv[3])
