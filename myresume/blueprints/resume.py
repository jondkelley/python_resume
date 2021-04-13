# Filename    : resume.py
# Author      : Jon Kelley <jonk@omg.lol>
# Description : Interactive online resume for jon-kelley.com


from flask import Blueprint, request
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Markup, Response, json, make_response
from flask import current_app as app
from flask import render_template, redirect, url_for, send_file
from json import load as json_load
from json import dumps as json_dumps
from myresume.sharedlib.jinja2 import get_current_datetime
from myresume.sharedlib.jinja2 import resume_date as filter_resume_date
from myresume.sharedlib.jinja2 import make_slug as filter_make_slug
import io
import jinja2
import markdown
import markdown.extensions.fenced_code
import mimetypes
from uuid import uuid4

myresume = Blueprint('myresume', __name__)
try:
    with open('/resume/resume.json', 'r') as outfile:
            resume = json_load(outfile)
except OSError as e:
    resume = {}


@myresume.route("/", methods=['GET', 'POST'])
def login():
    """
    Start page
    """
    if not resume:
        return render_template('noresume.html', resume=resume)
    return render_template('index.html', resume=resume)


@myresume.route("/terminal", methods=['GET', 'POST'])
def term():
    """
    terminal iframe
    """
    return render_template('term.html')


def generate_markdown():
    """
    generate resume in markdown format
    """
    jinja2.filters.FILTERS['resume_date'] = filter_resume_date
    jinja2.filters.FILTERS['make_slug'] = filter_make_slug
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("/resume/"))
    template = env.get_template("resume.md.jinja2")
    markdown = template.render(resume=resume, current_timestamp_utc=get_current_datetime(), uuid=uuid4())
    return markdown


@myresume.route("/resume.md/")
@myresume.route("/resume.md")
def resume_markdown():
    """
    generates a raw markdown document from resume
    """
    response = make_response(generate_markdown(), 200)
    response.mimetype = "text/plain"
    return response


@myresume.route("/resume.md/render/theme/<theme>")
@myresume.route("/resume.md/render")
def resume_markdown_theme(theme='3'):
    """
    generates a rendered markdown document from resume theme
    """
    html_body = markdown.markdown(generate_markdown(), extensions=[
                                  'fenced_code', 'codehilite'])
    stylesheet = f'<link rel="stylesheet" href="/static/css/markdown/markdown{theme}.css"/>'
    header = f"<head><title>⭐{resume['profile']['first_name']} {resume['profile']['last_name']} Resume - Markdown Render</title>{stylesheet}</head>"
    preface = '<p><strong><em>Click <a href="/resume.md/">here</a> for raw markdown.</em></strong></p>'
    return f'{header}\n\n{preface}{html_body}'

@myresume.route("/resume.json", methods=['GET', 'POST'])
def resume_json():
    """
    return resume in pretty JSON
    """
    print(resume)
    json = app.make_response(json_dumps(resume, indent=5))
    json.mimetype = "text/plain"
    return json

def retrieve_resume_from_pandoc_dir(sourcefile_path, sourcefile, filetype, name):
    """
    retrieve and send the specified resume from the pandoc directory
    """
    mimetype = mimetypes.guess_type(sourcefile)[0]
    with open(sourcefile, 'rb') as outfile:
    #with io.open(sourcefile, mode="rb", encoding="utf-8") as outfile:
        file = outfile.read()
        return send_file(
                     io.BytesIO(file),
                     attachment_filename=f'{name}_resume.{filetype}',
                     mimetype=mimetype
               )

@myresume.route('/download/resume.<filetype>')
def download_link(filetype=None):
    """
    loads a resume off the pandoc shared docker volume
    """
    sourcefile_path = '/pandoc/'
    name = 'jonathan_d_kelley'
    sourcefile = '{sourcefile_path}resume.{filetype}'
    if filetype == 'pdf':
        sourcefile = sourcefile.format(sourcefile_path=sourcefile_path,filetype=filetype)
        return retrieve_resume_from_pandoc_dir(sourcefile_path, sourcefile, filetype, name)
    elif filetype == 'epub':
        sourcefile = sourcefile.format(sourcefile_path=sourcefile_path,filetype=filetype)
        return retrieve_resume_from_pandoc_dir(sourcefile_path, sourcefile, filetype, name)
    elif filetype == 'tex':
        sourcefile = sourcefile.format(sourcefile_path=sourcefile_path,filetype=filetype)
        return retrieve_resume_from_pandoc_dir(sourcefile_path, sourcefile, filetype, name)
    elif filetype == 'docx':
        sourcefile = sourcefile.format(sourcefile_path=sourcefile_path,filetype=filetype)
        return retrieve_resume_from_pandoc_dir(sourcefile_path, sourcefile, filetype, name)
    elif filetype == 'odt':
        sourcefile = sourcefile.format(sourcefile_path=sourcefile_path,filetype=filetype)
        return retrieve_resume_from_pandoc_dir(sourcefile_path, sourcefile, filetype, name)
    #return render_template('download.html', filename=filename)

