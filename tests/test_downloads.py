
from requests import get
from os import environ
from time import sleep

if environ.get('CI_TEST'):
    # Give pandoc time to generate
    sleep(30)


class TestDownloads():
    """
    verifies to make sure the pandoc container is generating resumes,
    and that flask can serve them on their routes
    """

    def test_pandoc_pdf(self, wait_for_flask):
        request_session, api_url = wait_for_flask
        r = request_session.get(f'{api_url}pandoc/resume.pdf')
        assert r.status_code == 200
        assert '%PDF-1.5' in r.text

    def test_pandoc_epub(self, wait_for_flask):
        request_session, api_url = wait_for_flask
        r = request_session.get(f'{api_url}pandoc/resume.epub')
        assert r.status_code == 200
        assert 'mimetypeapplication/epub' in r.text

    def test_pandoc_tex(self, wait_for_flask):
        request_session, api_url = wait_for_flask
        r = request_session.get(f'{api_url}pandoc/resume.tex')
        assert r.status_code == 200
        assert 'begin{document}' in r.text

    def test_pandoc_docx(self, wait_for_flask):
        request_session, api_url = wait_for_flask
        r = request_session.get(f'{api_url}pandoc/resume.docx')
        assert r.status_code == 200
        assert '[Content_Types].xml' in r.text
        assert 'word/document.xml' in r.text

    def test_pandoc_odt(self, wait_for_flask):
        request_session, api_url = wait_for_flask
        r = request_session.get(f'{api_url}pandoc/resume.odt')
        assert r.status_code == 200
        assert 'mimetypeapplication/vnd.oasis.opendocument.text' in r.text

    def test_missing_download_template(self, wait_for_flask):
        """
        ensure missing file extensions shows the soft error page
        """
        request_session, api_url = wait_for_flask
        r = request_session.get(f'{api_url}pandoc/resume.bogus_extension')
        assert r.status_code == 200
        assert 'Cannot load /pandoc/resume.bogus' in r.text
