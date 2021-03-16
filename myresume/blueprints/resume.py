# Filename    : resume.py
# Author      : Jon Kelley <jonk@omg.lol>
# Description : Interactive online resume for jon-kelley.com

from flask import Blueprint, request
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Markup, Response, json, make_response, send_file
from flask import current_app as app
from flask import jsonify
from flask import render_template, redirect, url_for
from json import load as json_load
from myresume.sharedlib.docx import generate_docx
from myresume.sharedlib.jinja2 import get_current_datetime
from myresume.sharedlib.jinja2 import resume_date as filter_resume_date
import jinja2
import markdown
import markdown.extensions.fenced_code

myresume = Blueprint('myresume', __name__)

with open('/resume.json', 'r') as outfile:
    resume = json_load(outfile)


@myresume.route("/resume.json", methods=['GET', 'POST'])
def resume_json():
    """
    return resume object
    """
    return jsonify(resume)

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


def build_markdown():
    """
    build resume in markdown format
    """
    jinja2.filters.FILTERS['resume_date'] = filter_resume_date
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("/"))
    template = env.get_template("resume.md.jinja2")
    markdown = template.render(resume=resume, current_timestamp_utc=get_current_datetime())
    return markdown

def generate_markdown_as_html(md, theme=False):
    """
    generate resume in HTML from markdown
    """
    if theme:
        html_body = markdown.markdown(md, extensions=[
                                      'fenced_code', 'codehilite'])
        stylesheet = f'<link rel="stylesheet" href="/static/css/markdown/{theme}.css"/>'
        return f'{stylesheet}\n\n{html_body}'
    else:
        html_body = markdown.markdown(md)
        return html_body

@myresume.route("/resume.md")
def resume_markdown():
    """
    generates a rendered markdown document from resume
    """
    render = request.args.get('render', False)
    if not render:
        response = make_response(build_markdown(), 200)
        response.mimetype = "text/plain"
        return response
    else:
        theme = request.args.get('theme', 'markdown3')
        return generate_markdown_as_html(build_markdown(), theme)

@myresume.route("/resume.docx")
def resume_docx():
    """
    generates a rendered word document resume
    """
    return 'TODO: Working on some bugs with DOCX'
    #print(generate_markdown_as_html(build_markdown()))
    #generate_docx(generate_markdown_as_html(build_markdown()))
    #return send_file('/tmp/resume.docx', attachment_filename='jonathan_d_kelley_resume.dox')

