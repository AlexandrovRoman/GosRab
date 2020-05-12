import requests
from app import config


class TestVacancyListResource:
    def setup(self):
        self.login = "new_email@yandex.ru"
        self.password = "456asdf"
        host = f"{config.HOST}:{config.PORT}"  # or pfproject.herokuapp.com
        self.url = f"http://{host}/api/vacancy"
        self.entry_url = f"http://{host}/api/login"
        self.correct_offset = {'offset': 0}

        self.session = requests.Session()
        self.auth()

    def auth(self):
        assert self.session.get(f"{self.entry_url}/{self.login}/{self.password}").json() == {'authorization': 'OK'}

    def test_not_auth_request(self):
        self.session.delete(self.entry_url)
        assert self.session.get(self.url).json() == {
            'error': 'Login before using API'}

    def test_get(self):
        assert list(self.session.get(self.url).json().keys()) == ["vacancy"]

    def test_with_arg_get(self):
        assert list(self.session.get(self.url, json=self.correct_offset).json().keys()) == ["vacancy"]
