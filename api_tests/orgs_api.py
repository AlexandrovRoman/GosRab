import requests
from app import config


class TestOrganizationResource:
    def setup(self):
        self.login = "new_email@yandex.ru"
        self.password = "456asdf"
        host = f"{config.HOST}:{config.PORT}"  # or pfproject.herokuapp.com
        self.url = f"http://{host}/api/organization"
        self.entry_url = f"http://{host}/api/login"

        self.session = requests.Session()
        self.auth()

    def auth(self):
        assert self.session.get(f"{self.entry_url}/{self.login}/{self.password}").json() == {'authorization': 'OK'}


class TestOrganizationResourceGet(TestOrganizationResource):
    def setup(self):
        super().setup()

        self.exist_org_id = 1
        self.nonexistent_org_id = 496328389432075595498547984397390890823082302312318042380432

    def test_get_by_not_auth_session(self):
        self.session.delete(self.entry_url)
        assert self.session.get(f"{self.url}/{self.exist_org_id}").json() == {'error': 'Login before using API'}

    def test_get_by_valid_id(self):
        assert list(self.session.get(f"{self.url}/{self.exist_org_id}").json().keys()) == ['organization']

    def test_get_by_invalid_id(self):
        assert self.session.get(f"{self.url}/{self.nonexistent_org_id}").status_code == 404


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
            self.session.delete(f"{self.url}/{self.current_org_id}/{self.current_org_jwt}").json()
        self.session.delete(self.entry_url)


class TestOrganizationResourceDelete(TestOrganizationResource):
    def setup(self):
        super().setup()

        self.nonexistent_org_id = 496328389432075595498547984397390890823082302312318042380432
        self.exist_org_id = 1
        self.wrong_jwt = 'aaa'

        self.my_org_id = None
        self.correct_jwt = ''

        self.test_org_json = {
            "name": "Пример INC.",
            "org_type": 'OAO',
            "org_desc": 'For tests'
        }

    def test_delete_not_exist_org(self):
        assert self.session.delete(f"{self.url}/{self.nonexistent_org_id}/{self.wrong_jwt}").status_code == 404

    def test_wrong_jwt(self):
        assert self.session.delete(f"{self.url}/{self.exist_org_id}/{self.wrong_jwt}").json() == {
            'error': 'delete is not allowed to this organization'}

    def test_correct_jwt(self):
        json = self.session.post(self.url, json=self.test_org_json).json()
        if 'organization' in json.keys():
            self.correct_jwt = json['organization']['api_token']
            self.my_org_id = json['organization']['id']
        assert self.session.delete(f"{self.url}/{self.my_org_id}/{self.correct_jwt}").json() == {'deleting': 'OK'}
