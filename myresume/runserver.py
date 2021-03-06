# Filename    : runserver.py
# Author      : Jon Kelley <jonk@omg.lol>
# Description : Interactive online resume for jon-kelley.com

from flask import Blueprint, Flask, request, session, g, redirect, url_for, abort, render_template, flash, Markup, Response, json, make_response, send_file
from myresume.blueprints.resume import myresume
from myresume.sharedlib.jinja2 import split_list_one, split_list_two, reverse_string, resume_date, calculate_age, make_slug
import base64
import os

app = Flask(__name__)

# key for cookie safety. Shal be overridden using ENV var SECRET_KEY
app.secret_key = os.getenv(
    "SECRET_KEY", "lasfuoi3ro8w7gfow3bwiubdwoeg7p23r8g23rg")

app.register_blueprint(myresume)


@app.template_filter('urlsafe_base64')
def urlsafe_base64_encode(s):
    if isinstance(s, 'Markup'):
        s = s.unescape()
    s = base64.urlsafe_b64encode(s.encode("utf8"))
    return Markup(s.decode("utf8"))


@app.template_filter('split_list_one')
def app_split_list_one(a_list):
    return split_list_one(a_list)


@app.template_filter('split_list_two')
def app_split_list_two(b_list):
    """ takes a list and returns the second half """
    return split_list_two(b_list)


@app.template_filter('revstr')
def app_reverse_string(s):
    """
    reversed a text string, I'm using this to prevent spam with email addresses or phone
    """
    return reverse_string(s)


@app.template_filter('resume_date')
def app_resume_date(strtime):
    """ cast a date like 2020-03-01 for the resume to March 2020"""
    return resume_date(strtime)


@app.template_filter('calculate_age')
def app_calculate_age(born):
    """ convert a date like 2020-03-01 into the number of days passed until today """
    return calculate_age(born)


@app.template_filter('make_slug')
def app_make_slug(text):
    """ make a slug for anchor links """
    return make_slug(text)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('500.html'), 500


def main():
    app.run(host='0.0.0.0', debug=False, port=5001, threaded=True)


if __name__ == '__main__':
    main()
