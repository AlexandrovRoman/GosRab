import requests
from app import config


class TestUserResource:
    def setup(self):
        self.login = "new_email@yandex.ru"
        self.password = "456asdf"
        host = f"{config.HOST}:{config.PORT}"  # or pfproject.herokuapp.com
        self.url = f"http://{host}/api/user"
        self.entry_url = f"http://{host}/api/login"

        self.session = requests.Session()
        self.auth()

    def auth(self):
        assert self.session.get(f"{self.entry_url}/{self.login}/{self.password}").json() == {'authorization': 'OK'}


class TestUserResourcePost(TestUserResource):
    def setup(self):
        super().setup()
        self.current_user_id = None
        # Какие стандарты для пароля и можно ли использовать латинцу в ФИО?
        self.valid_json = {
            "name": "Пример",
            "surname": "Пример",
            "fathername": "Иванов",
            "email": "right@email.com",
            "password": "abc123"
        }

        self.invalid_json = [{
            "name": "123123",
            "surname": "Aaaa",
            "fathername": "aa222",
            "email": "uncorremailcom",
            "password": "hmm"
        }, {
            "name": "aaaa",
            "surname": "123",
            "fathername": "aa222",
            "email": "unco.rremail@com",
            "password": "hmm2"
        }]

    def test_not_auth_request(self):
        self.session.delete(self.entry_url)
        assert self.session.post(self.url, json=self.valid_json).json() == {
            'error': 'Login before using API'}

    def test_valid_data(self):
        json = self.session.post(self.url, json=self.valid_json).json()
        if 'user' in json.keys():
            self.current_user_id = json['user']['id']
        print(json)
        assert list(json.keys())[0] == 'adding' and json['adding'] == 'OK'

    def test_invalid_email(self):
        json = self.valid_json.copy()
        json["email"] = "email@emai.com"
        assert self.session.post(self.url, json=json).json() == {'error': 'email already taken'}

    def test_invalid_data(self):
        # Когда параметры не валидны
        for data in self.invalid_json:
            assert list(self.session.post(self.url, json=data).json().keys()) == ['error']

    def teardown(self):
        self.session.get(f"{self.entry_url}/{self.valid_json['email']}/{self.valid_json['password']}")
        if self.current_user_id:
            self.session.delete(f'{self.url}/{self.current_user_id}')
        self.session.delete(self.entry_url)


class TestUserResourceGet(TestUserResource):
    def setup(self):
        super().setup()

        self.exist_user_id = 1
        self.nonexistent_user_id = 496328389432075595498547984397390890823082302312318042380432

    def test_get_by_not_auth_session(self):
        self.session.delete(self.entry_url)
        assert self.session.get(f"{self.url}/{self.exist_user_id}").json() == {'error': 'Login before using API'}

    def test_get_by_valid_id(self):
        assert list(self.session.get(f"{self.url}/{self.exist_user_id}").json()["user"].keys()) == \
               ['birth_date', 'fathername', 'id', 'name', 'surname']

    def test_get_by_invalid_id(self):
        assert self.session.get(f"{self.url}/{self.nonexistent_user_id}").status_code == 404


class TestUserResourceDelete(TestUserResource):
    def setup(self):
        super().setup()

        self.not_exist_user_id = 626234862472437980238023408282439073287438
        self.alien_user_id = 1

        # Создаем пользователя и присваиваем его id данной переменной
        self.current_user_id = None

        self.test_user_json = {
            "name": "Пример",
            "surname": "Пример",
            "fathername": "Иванов",
            "email": "corecty@email.com",
            "password": "abc123"
        }

    def test_delete_not_exist_account(self):
        assert self.session.delete(f"{self.url}/{self.not_exist_user_id}").status_code == 404

    def test_delete_alien_account(self):
        assert self.session.delete(f"{self.url}/{self.alien_user_id}").json() == \
               {'error': 'delete is not allowed to this user'}

    def test_delete_my_account(self):
        json = self.session.post(self.url, json=self.test_user_json).json()
        if 'user' in json.keys():
            self.current_user_id = json['user']['id']
        self.session.get(f"{self.entry_url}/{self.test_user_json['email']}/{self.test_user_json['password']}")
        assert self.session.delete(f"{self.url}/{self.current_user_id}").json() == {'deleting': 'OK'}
