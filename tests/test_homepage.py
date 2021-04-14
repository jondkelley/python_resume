from requests import get


def test_index_loads(wait_for_flask):
    request_session, api_url = wait_for_flask
    r = request_session.get(f'{api_url}')
    assert r.status_code == 200


def test_index_contains_html(wait_for_flask):
    request_session, api_url = wait_for_flask
    r = request_session.get(f'{api_url}')
    assert r.status_code == 200
    assert '<html lang="en">' in r.text


def test_static_favicon(wait_for_flask):
    request_session, api_url = wait_for_flask
    r = request_session.get(f'{api_url}static/images/favicon.ico')
    assert r.status_code == 200


def test_static_bootstrap_css(wait_for_flask):
    request_session, api_url = wait_for_flask
    r = request_session.get(f'{api_url}static/css/bootstrap.min.css')
    assert r.status_code == 200


def test_static_custom_css(wait_for_flask):
    request_session, api_url = wait_for_flask
    r = request_session.get(f'{api_url}static/css/style.css')
    assert r.status_code == 200
