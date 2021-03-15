from datetime import datetime, timedelta
from flask import Blueprint, request
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Markup, Response, json
from flask import current_app as app
from flask import render_template, redirect, url_for
from json import loads as json_loads
from rebrow.sharedlib.metadata import serverinfo_meta
from redis.exceptions import ConnectionError
from redis.sentinel import Sentinel
import base64
import os
import redis
import time

rebrow = Blueprint('rebrow', __name__)

with open('/resume.json', 'r') as outfile:
    resume = json.load(outfile)


@rebrow.route("/", methods=['GET', 'POST'])
def login():
    """
    Start page
    """
    return render_template('index.html', resume=resume)

