# Filename    : resume.py
# Author      : Jon Kelley <jonk@omg.lol>
# Description : Interactive online resume for jon-kelley.com

from datetime import datetime, timedelta
from flask import Blueprint, request
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Markup, Response, json, make_response
from flask import current_app as app
from flask import jsonify
from flask import render_template, redirect, url_for
from json import load as json_load
from myresume.sharedlib.jinja2 import resume_date as filter_resume_date
import jinja2
import markdown
import markdown.extensions.fenced_code

myresume = Blueprint('myresume', __name__)

with open('/resume.json', 'r') as outfile:
    resume = json_load(outfile)


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


def generate_markdown():
    """
    generate resume in markdown format
    """
    jinja2.filters.FILTERS['resume_date'] = filter_resume_date
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("/"))
    template = env.get_template("resume.md.jinja2")
    markdown = template.render(resume=resume)
    return markdown


@myresume.route("/resume.md")
def resume_markdown():
    """
    generates a rendered markdown document from resume
    """
    theme = request.args.get('theme', 'markdown3')
    render = request.args.get('render', False)
    if not render:
        response = make_response(generate_markdown(), 200)
        response.mimetype = "text/plain"
        return response
    else:
        html_body = markdown.markdown(generate_markdown(), extensions=[
                                      'fenced_code', 'codehilite'])
        stylesheet = f'<link rel="stylesheet" href="/static/css/markdown/{theme}.css"/>'
        return f'{stylesheet}\n\n{html_body}'


@myresume.route("/resume.pdf")
def resume_pdf():
    """
    generates a rendered PDF file from a markdown base
    """
    theme = request.args.get('theme', 'markdown3')
    render = request.args.get('render', False)
    html_body = markdown.markdown(generate_markdown(), extensions=[
                                  'fenced_code', 'codehilite'])
    stylesheet = f'<link rel="stylesheet" href="/static/css/markdown/{theme}.css"/>'
    return f'{stylesheet}\n\n{html_body}'


@myresume.route("/resume.json", methods=['GET', 'POST'])
def resume_json():
    """
    Return resume in pretty JSON
    """
    return jsonify(resume)
