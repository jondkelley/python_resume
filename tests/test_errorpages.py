from requests import get


def test_404(wait_for_flask):
    request_session, api_url = wait_for_flask
    res = request_session.get(f'{api_url}404')
    assert res.status_code == 404
    assert '<a href="/" target="_blank">' in res.text
