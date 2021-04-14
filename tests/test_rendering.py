from requests import get


def test_resume_update_endpoint_security(wait_for_flask, update_secret):
    """
    ensure resume.json update security works around the update endpoint
    """
    request_session, api_url = wait_for_flask
    r = request_session.get(f'{api_url}resume/update?secret={update_secret}')
    assert r.status_code == 200
    rjson = r.json()
    assert rjson['status'] == 'updated'


def test_resume_update_endpoint_security_unauthorized(wait_for_flask, update_secret):
    """
    ensure resume.json update security works when an INVALID_SECRET is provided
    """
    request_session, api_url = wait_for_flask
    r = request_session.get(
        f'{api_url}resume/update?secret=INVALID_SECRET_{update_secret}')
    assert r.status_code == 401
    rjson = r.json()
    assert rjson['status'] == 'unauthorized'


class TestRenderedJinjaStructure():
    """
    verifies to make sure the jinja templates are rendering fields properly using test.resume.json
    """

    def test_setup(self, wait_for_flask, update_secret):
        url = 'https://raw.githubusercontent.com/jondkelley/python_resume/master/tests/testdata/test.resume.json'
        request_session, api_url = wait_for_flask
        r = request_session.get(
            f'{api_url}resume/update?secret={update_secret}&url={url}')
        assert r.status_code == 200
        rjson = r.json()
        assert rjson['status'] == 'updated'

    def test_index_contains_splash_name(self, wait_for_flask):
        request_session, api_url = wait_for_flask
        r = request_session.get(f'{api_url}')
        assert r.status_code == 200
        assert '<h1 class="glitch" data-text="John &#34;Test&#34; Doe">John &#34;Test&#34; Doe</h1>' in r.text

    def test_index_contains_profile_tagline(self, wait_for_flask):
        request_session, api_url = wait_for_flask
        r = request_session.get(f'{api_url}')
        assert r.status_code == 200
        assert '<p class="lead">My hipster tagline</p>' in r.text

    def test_index_contains_profile_about_me(self, wait_for_flask):
        request_session, api_url = wait_for_flask
        r = request_session.get(f'{api_url}')
        assert r.status_code == 200
        assert 'About me.' in r.text

    def test_index_contains_profile_age(self, wait_for_flask):
        request_session, api_url = wait_for_flask
        r = request_session.get(f'{api_url}')
        assert r.status_code == 200
        assert '<strong>Age:</strong><br />121 years old<br />' in r.text

    def test_index_contains_profile_location(self, wait_for_flask):
        request_session, api_url = wait_for_flask
        r = request_session.get(f'{api_url}')
        assert r.status_code == 200
        assert 'Somewhere, Someplace, USA, Earth' in r.text

    def test_index_contains_profile_location(self, wait_for_flask):
        request_session, api_url = wait_for_flask
        r = request_session.get(f'{api_url}')
        assert r.status_code == 200
        assert 'Somewhere, Someplace, USA, Earth' in r.text

    def test_index_contains_experiences_company(self, wait_for_flask):
        request_session, api_url = wait_for_flask
        r = request_session.get(f'{api_url}')
        assert r.status_code == 200
        assert '<h4 id="megacorp-codejockey">MegaCorp</h4>' in r.text
        assert '<h4 id="tinyllc-codebarista">TinyLLC</h4>' in r.text

    def test_index_contains_experiences_titles(self, wait_for_flask):
        request_session, api_url = wait_for_flask
        r = request_session.get(f'{api_url}')
        assert r.status_code == 200
        assert '<strong><a class="pilcrow-experience" href="#megacorp-codejockey">¶</a> Codejockey</strong>' in r.text
        assert '<strong><a class="pilcrow-experience" href="#tinyllc-codebarista">¶</a> CodeBarista</strong>' in r.text

    def test_index_contains_experiences_links(self, wait_for_flask):
        request_session, api_url = wait_for_flask
        r = request_session.get(f'{api_url}')
        assert r.status_code == 200
        assert '<a href="http://megacorp.local" target="_blank">http://megacorp.local</a>' in r.text
        assert '<a href="http://tinycorp.local" target="_blank">http://tinycorp.local</a>' in r.text

    def test_index_contains_abilities_hypervisors(self, wait_for_flask):
        request_session, api_url = wait_for_flask
        r = request_session.get(f'{api_url}')
        assert r.status_code == 200
        assert '<span class="ability-title">Hypervisor 1</span>' in r.text
        assert '<span class="ability-title">Hypervisor 2</span>' in r.text

    def test_index_contains_projects(self, wait_for_flask):
        request_session, api_url = wait_for_flask
        r = request_session.get(f'{api_url}')
        assert r.status_code == 200
        assert '<h4>project_name</h4>' in r.text
        assert '<p><strong>Flashy tagline</strong></br>' in r.text

    def test_index_contains_publications(self, wait_for_flask):
        request_session, api_url = wait_for_flask
        r = request_session.get(f'{api_url}')
        assert r.status_code == 200
        assert '<strong>My first blog article.</strong>' in r.text
        assert 'My very first blog article where I learned how to write a blog!' in r.text
        assert '#unit #test' in r.text
