# encoding: utf8

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Markup, Response, json
from myresume.blueprints.resume import myresume
import os
import base64
import datetime

app = Flask(__name__)

# key for cookie safety. Shal be overridden using ENV var SECRET_KEY
app.secret_key = os.getenv(
    "SECRET_KEY", "lasfuoi3ro8w7gfow3bwiubdwoeg7p23r8g23rg")

app.register_blueprint(myresume)


@app.template_filter('urlsafe_base64')
def urlsafe_base64_encode(s):
    if type(s) == 'Markup':
        s = s.unescape()
    s = base64.urlsafe_b64encode(s.encode("utf8"))
    return Markup(s.decode("utf8"))

@app.template_filter('split_list_one')
def split_list_one(a_list):
    """ takes a list and returns the first half """
    half = len(a_list)//2
    return a_list[:half]

@app.template_filter('split_list_two')
def split_list_two(a_list):
    """ takes a list and returns the second half """
    half = len(a_list)//2
    return a_list[half:]

@app.template_filter('revstr')
def reverse_string(s):
	"""
	reversed a text string, I'm using this to prevent spam with email addresses or phone
	"""
	return s[::-1]

@app.template_filter('resume_date')
def resume_date(strtime):
    """ cast a date like 2020-03-01 for the resume to March 2020"""
    if not strtime:
        return 'current'
    datetime_object = datetime.datetime.strptime(strtime, '%Y-%m-%d')
    return f'{datetime_object:%B %Y}'

@app.template_filter('calculate_age')
def calculate_age(born):
    """ convert a date like 2020-03-01 into the number of days passed until today """
    born = datetime.date(int(born.split('-')[0]), int(born.split('-')[1]), int(born.split('-')[2]))
    today = datetime.date.today() 
    try:  
        birthday = born.replace(year = today.year) 
  
    # raised when birth date is February 29 
    # and the current year is not a leap year 
    except ValueError:  
        birthday = born.replace(year = today.year, 
                  month = born.month + 1, day = 1) 
  
    if birthday > today: 
        return today.year - born.year - 1
    else:
        return today.year - born.year 

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

def main():
    app.run(host="0.0.0.0", debug=False, port=5001, threaded=True)


if __name__ == "__main__":
    main()
