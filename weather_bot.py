import sys, os
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
	apiKey = '1473eef1c8584998'
	base_url = 'http://api.wunderground.com/api/{}/history_{}/q/KNYC.json'

	sdate = pd.to_datetime(start_date)
	edate = pd.to_datetime(end_date)

	# -- for each day
	for i in range((edate - sdate).days):

		query = base_url.format(apiKey, sdate.strftime('%Y%m%d'))
		print 'Weatherbot: fetching {}'.format(query)
    
		r = requests.get(query)
		
		df = pd.DataFrame(r.json()['history']['observations'])

		df['date'] = df['date'].map(lambda x: x['pretty'])
		
		file_exists = os.path.isfile(fpath)
		with open(fpath,"a") as f:
			if not file_exists:
				df.to_csv(f, header=True, index=False)

			df.to_csv(f, header=False, index=False)
		
		sdate += datetime.timedelta(days=1)
	print "Finished!"

if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2], sys.argv[3])
