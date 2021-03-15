import datetime


def get_years_age(born):
	before = datetime.datetime.strptime(born,'%m/%d/%Y')
	now = datetime.datetime.now()
	float((now-before))
	#return float((now-before).days)/365