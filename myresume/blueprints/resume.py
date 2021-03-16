from datetime import datetime, timedelta
from flask import Blueprint, request
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Markup, Response, json, make_response
from flask import current_app as app
from flask import render_template, redirect, url_for
from json import load as json_load
from flask import jsonify

from myresume.sharedlib.jinja2 import resume_date as filter_resume_date
import markdown
import markdown.extensions.fenced_code
import jinja2

myresume = Blueprint('myresume', __name__)

with open('/resume.json', 'r') as outfile:
    resume = json_load(outfile)

def generate_markdown():
    jinja2.filters.FILTERS['resume_date'] = filter_resume_date
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("/"))
    template = env.get_template("resume.md.jinja2")
    markdown = template.render(resume=resume)
    return markdown

@myresume.route("/", methods=['GET', 'POST'])
def login():
    """
    Start page
    """
    return render_template('index.html', resume=resume)

@myresume.route("/terminal", methods=['GET', 'POST'])
def term():
    """
    Terminal
    """
    return render_template('term.html')

@myresume.route("/resume.md")
def serve_markdown():
    """
    generates a rendered markdown document from resume
    """
    markdown = generate_markdown()
    response = make_response(markdown, 200)
    response.mimetype = "text/plain"
    return response

@myresume.route("/resume.md/render")
def serve_markdown_rendered():
    """
    generate rendered markdown
    """
    html = markdown.markdown(generate_markdown(), extensions=['fenced_code', 'codehilite'])
    return html

@myresume.route("/resume.json", methods=['GET', 'POST'])
def resume_json():
    """
    Return resume in pretty JSON
    """
    return jsonify(resume)
