from requests import get


def test_markdown_theme_render(wait_for_flask):
    request_session, api_url = wait_for_flask
    r = request_session.get(f'{api_url}resume.md/render/theme/8')
    assert r.status_code == 200


def test_markdown_template(wait_for_flask):
    request_session, api_url = wait_for_flask
    r = request_session.get(f'{api_url}resume.md/')
    assert r.status_code == 200
    r = request_session.get(f'{api_url}resume.md')
    assert r.status_code == 200
