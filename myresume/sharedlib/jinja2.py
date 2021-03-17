# Filename    : jinja2.py
# Author      : Jon Kelley <jonk@omg.lol>
# Description : Interactive online resume for jon-kelley.com

import datetime
from slugify import slugify

# Custom jinja2 globals


def get_current_datetime():
    utc_timestamp = datetime.datetime.utcnow()

    return f'{utc_timestamp} (UTC)'


# Custom jinja2 filters


def split_list_one(a_list):
    """ takes a list and returns the first half """
    half = len(a_list)//2
    return a_list[:half]


def split_list_two(a_list):
    """ takes a list and returns the second half """
    half = len(a_list)//2
    return a_list[half:]


def reverse_string(s):
    """
    reversed a text string, I'm using this to prevent spam with email addresses or phone
    """
    return s[::-1]


def resume_date(strtime):
    """ cast a date like 2020-03-01 for the resume to March 2020"""
    if not strtime:
        return 'Current'
    datetime_object = datetime.datetime.strptime(strtime, '%Y-%m-%d')
    return f'{datetime_object:%B %Y}'


def calculate_age(born):
    """ convert a date like 2020-03-01 into the number of days passed until today """
    born = datetime.date(
        int(born.split('-')[0]), int(born.split('-')[1]), int(born.split('-')[2]))
    today = datetime.date.today()
    try:
        birthday = born.replace(year=today.year)

    # raised when birth date is February 29
    # and the current year is not a leap year
    except ValueError:
        birthday = born.replace(year=today.year,
                                month=born.month + 1, day=1)

    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year


def make_slug(text):
    return slugify(text)