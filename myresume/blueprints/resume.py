# Filename    : resume.py
# Author      : Jon Kelley <jonk@omg.lol>
# Description : Interactive online resume for jon-kelley.com


from flask import Blueprint, Flask, request, session, g, redirect, url_for, abort, render_template, flash, Markup, Response, json, make_response, send_file
from flask import current_app as app
from json import load as json_load
from json import dumps as json_dumps
from json import loads as json_loads
from myresume.sharedlib.jinja2 import get_current_datetime
from myresume.sharedlib.jinja2 import resume_date as filter_resume_date
from myresume.sharedlib.jinja2 import make_slug as filter_make_slug
from os import environ, path, walk
from uuid import uuid4
import io
import jinja2
import markdown
import mimetypes
import urllib.request

myresume = Blueprint('myresume', __name__)


class ResumeSingleton:
    """
    singleton instance to manage the resume, this allows me do in-app updates
    of resume content from github without having to rebuild the whole
    container with the static resume.json content, extremely useful if
    tailoring the resume to a specific job application or company
    """
    __instance = None

    @staticmethod
    def get_instance():
        """
        return singleton instance
        """
        if ResumeSingleton.__instance is None:
            ResumeSingleton()
        return ResumeSingleton.__instance

    def resume(self):
        """
        return the current resume data
        """
        return self.resume

    def refresh_resume(self, url):
        """
        refresh resume off github content
        """
        if not url:
            url = 'https://raw.githubusercontent.com/jondkelley/python_resume/master/resume.json'
        req = urllib.request.Request(url)
        r = urllib.request.urlopen(req).read()
        self.resume = json_loads(r.decode('utf-8'))

    def __init__(self):
        """
        private constructor
        """
        if ResumeSingleton.__instance is not None:
            raise Exception(
                "This class is a singleton, don't use parenthesis!")
        else:
            ResumeSingleton.__instance = self
            try:
                # load resume from docker image on startup
                with open('/resume/resume.json', 'r') as outfile:
                    self.resume = json_load(outfile)
            except OSError as e:
                # if container is missing resume content, load from github
                self.refresh_resume()


resume_instance = ResumeSingleton()


@myresume.route('/resume/update')
def update():
    """
    update my resume with newer content from github without requiring full container rebuild
    """
    resume_url = request.args.get('url', None)
    secret = request.args.get('secret', False)
    config_secret = environ.get('UPDATE_SECRET', True)
    if secret == config_secret:
        cv = ResumeSingleton.get_instance()
        cv.refresh_resume(resume_url)
        response = {"status": "updated", "resume": cv.resume}
        json = app.make_response(json_dumps(response, indent=5))
        json.mimetype = "text/plain"
        return json
    else:
        response = {"status": "unauthorized",
                    "reason": "bad or missing secret"}
        json = app.make_response(json_dumps(response, indent=5))
        json.mimetype = "text/plain"
        return json, 401


@myresume.route('/')
def home():
    """
    home page
    """
    cv = ResumeSingleton.get_instance()
    if not cv.resume:
        return render_template('nojson.html', resume=cv.resume)
    return render_template('index.html', resume=cv.resume)


@myresume.route('/terminal')
def term():
    """
    terminal iframe page
    """
    return render_template('term.html')


def generate_markdown():
    """
    generate resume in markdown
    """
    cv = ResumeSingleton.get_instance()
    jinja2.filters.FILTERS['resume_date'] = filter_resume_date
    jinja2.filters.FILTERS['make_slug'] = filter_make_slug
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("/resume/"))
    template = env.get_template("resume.md.jinja2")
    markdown = template.render(
        resume=cv.resume,
        current_timestamp_utc=get_current_datetime(),
        uuid=uuid4())
    return markdown


@myresume.route('/resume.md/')
@myresume.route('/resume.md')
def resume_markdown():
    """
    generates a raw markdown resume
    """
    response = make_response(generate_markdown(), 200)
    response.mimetype = "text/plain"
    return response


@myresume.route('/resume.md/render/theme/<theme>')
@myresume.route('/resume.md/render')
def resume_markdown_theme(theme='3'):
    """
    generates a *rendered* markdown themed resume, defaults to theme 3
    """
    cv = ResumeSingleton.get_instance()
    resume = cv.resume
    html_body = markdown.markdown(generate_markdown(), extensions=[
                                  'fenced_code', 'codehilite'])
    stylesheet = f'<link rel="stylesheet" href="/static/css/markdown/markdown{theme}.css"/>'
    header = f"<head><title>⭐{resume['profile']['first_name']} {resume['profile']['last_name']} Resume - Markdown Render</title>{stylesheet}</head>"
    preface = '<p><strong><em>Click <a href="/resume.md/">here</a> for raw markdown.</em></strong></p>'
    return f'{header}\n\n{preface}{html_body}'


@myresume.route('/resume.json')
def resume_json():
    """
    return resume in pretty JSON
    """
    cv = ResumeSingleton.get_instance()
    resume = cv.resume
    json = app.make_response(json_dumps(resume, indent=5))
    json.mimetype = "text/plain"
    return json


def render_from_pandoc_dir(sourcefile_path, sourcefile, filetype, name):
    """
    retrieve and send the specified resume from the pandoc directory
    """
    mimetype = mimetypes.guess_type(sourcefile)[0]
    with open(sourcefile, 'rb') as outfile:
        # with io.open(sourcefile, mode="rb", encoding="utf-8") as outfile:
        file = outfile.read()
        return send_file(
            io.BytesIO(file),
            attachment_filename=f'resume.{filetype}',
            mimetype=mimetype
        )


@myresume.route('/pandoc/resume.<filetype>')
def download_link(filetype=None):
    """
    download a resume from the pandoc shared docker volume
    """
    sourcefile_path = '/pandoc/'
    name = 'jonathan_d_kelley'
    sourcefile = f'{sourcefile_path}resume.{filetype}'

    if not path.exists(sourcefile):
        _, _, available_files = next(walk(sourcefile_path))
        return render_template(
            'nofile.html',
            filename=sourcefile,
            files=available_files)
    else:
        return render_from_pandoc_dir(
            sourcefile_path, sourcefile, filetype, name)


@myresume.route('/500')
def internal_server_error():
    """
    raise exception to display 500 error page
    """
    raise Exception('500 error test')
