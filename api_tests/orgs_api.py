import requests
from app import config


class TestOrganizationResource:
    def setup(self):
        self.login = "new_email@yandex.ru"
        self.password = "456asdf"

        self.login_org_id = 1
        self.password_org_jwt = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.' \
                                'eyJwYXlsb2FkIjoiXHUwNDFlXHUwNDQwXHUwNDMzXHUwNDMwXHUwNDNkXHUwNDM4XHUwNDM3XHUwNDMwX' \
                                'HUwNDQ2XHUwNDM4XHUwNDRmIDEiLCJpYXQiOjE1ODkyNjYyNjEsImV4cCI6MTU4OTg3MTA2MX0.' \
                                'imoepJ11Hbd5mhhTVIDBiJv-pjdpt6oh3y3TyUkYPDc'

        host = f"{config.HOST}:{config.PORT}"  # or pfproject.herokuapp.com
        self.url = f"http://{host}/api/organization"
        self.entry_url = f"http://{host}/api/login"
        self.org_entry_url = f"http://{host}/api/org_login"

        self.session = requests.Session()
        self.auth()
        self.org_auth()

    def auth(self):
        assert self.session.get(f"{self.entry_url}/{self.login}/{self.password}").json() == {'authorization': 'OK'}

    def org_auth(self):
        assert self.session.get(f"{self.org_entry_url}/{self.login_org_id}/{self.password_org_jwt}").json() == {
            'authorization': 'OK'}


class TestOrganizationResourceGet(TestOrganizationResource):
    def setup(self):
        super().setup()

        self.exist_org_id = 1
        self.nonexistent_org_id = 496328389432075595498547984397390890823082302312318042380432

    def test_get_by_not_auth_session(self):
        self.session.delete(self.org_entry_url)
        assert self.session.get(f"{self.url}").json() == {
            'error': 'Login with your organization before using Organizations API'}

    def test_get(self):
        assert list(self.session.get(f"{self.url}").json().keys()) == ['organization']


class TestOrganizationResourcePost(TestOrganizationResource):
    def setup(self):
        super().setup()
        self.current_org_id = None
        self.current_org_jwt = ''

        self.valid_json = {
            "name": "Пример INC.",
            "org_type": 'OAO',
            "org_desc": 'For tests'
        }

        # Что считается недопустимым для имени,типа и описания организации?
        self.invalid_json = []

    def test_not_auth_request(self):
        self.session.delete(self.entry_url)
        assert self.session.post(self.url, json=self.valid_json).json() == {
            'error': 'Login before using API'}

    def test_valid_data(self):
        json = self.session.post(self.url, json=self.valid_json).json()
        if 'organization' in json.keys():
            self.current_org_id = json['organization']['id']
            self.current_org_jwt = json['organization']['api_token']
        assert list(json.keys())[0] == 'adding' and json['adding'] == 'OK'

    def teardown(self):
        if self.current_org_jwt and self.current_org_id:
            self.session.get(f"{self.org_entry_url}/{self.current_org_id}/{self.current_org_jwt}").json()
            self.session.delete(f"{self.url}").json()
        self.session.delete(self.entry_url)


class TestOrganizationResourceDelete(TestOrganizationResource):
    def setup(self):
        super().setup()

        self.wrong_jwt = 'aaa'

        self.my_org_id = None
        self.correct_jwt = ''

        self.test_org_json = {
            "name": "Пример INC.",
            "org_type": 'OAO',
            "org_desc": 'For tests'
        }

    def test_correct_jwt(self):
        json = self.session.post(self.url, json=self.test_org_json).json()
        if 'organization' in json.keys():
            self.correct_jwt = json['organization']['api_token']
            self.my_org_id = json['organization']['id']
        self.session.get(f"{self.org_entry_url}/{self.my_org_id}/{self.correct_jwt}").json()
        assert self.session.delete(f"{self.url}").json() == {'deleting': 'OK'}
