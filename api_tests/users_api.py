import requests
from app import config


class TestUserResource:
    def setup(self):
        self.login = ""
        self.password = ""
        host = f"{config.HOST}:{config.PORT}"  # or pfproject.herokuapp.com
        self.url = f"http://{host}/api/user"

    def auth(self):
        # Создаем пользовательскую сессию
        pass


class TestUserResourcePost(TestUserResource):
    def setup(self):
        super().setup()

        self.valid_json = {
            "name": "",
            "surname": "",
            "fathername": "",
            "email": "",
            "password": ""
        }

        self.invalid_json = {
            "name": "",
            "surname": "",
            "fathername": "",
            "email": "",
            "password": ""
        }

    def test_not_auth_request(self):
        pass

    def test_valid_data(self):
        assert requests.post(self.url, json=self.valid_json).json() == {'adding': 'OK'}

    def test_invalid_email(self):
        json = self.valid_json.copy()
        json["email"] = "email@emai.com"
        assert requests.post(self.url, json=json).json() == {'adding': 'OK'}

    def test_invalid_data(self):
        # Когда параметры не валидны
        assert requests.post(self.url, json=self.invalid_json).json() == {}

    def teardown(self):
        # Удаляем созданного пользователя
        pass


class TestUserResourceGet(TestUserResource):
    def setup(self):
        self.exist_user_id = 1
        self.nonexistent_user_id = 496328389432075595498547984397390890823082302312318042380432

    def test_get_by_not_auth_session(self):
        pass

    def test_get_by_valid_id(self):
        assert requests.get(f"{self.url}/{self.exist_user_id}").json()["user"].keys() == \
               ('id', 'name', 'surname', 'fathername', 'birth_date')

    def test_get_by_invalid_id(self):
        assert requests.get(f"{self.url}/{self.exist_user_id}").status_code == 404


class TestUserResourceDelete(TestUserResource):
    def setup(self):
        super().setup()

        self.not_exist_user_id = 626234862472437980238023408282439073287438
        self.alien_user_id = 1

        # Создаем пользователя и присваиваем его id данной переменной
        self.current_user_id = 1

    def test_delete_not_exist_account(self):
        assert requests.delete(f"{self.url}/{self.not_exist_user_id}").status_code == 404

    def test_delete_alien_account(self):
        assert requests.delete(f"{self.url}/{self.current_user_id}").json() == \
               {'deleting': 'Operation not allowed to this user'}

    def test_delete_my_account(self):
        assert requests.delete(f"{self.url}/{self.current_user_id}").json() == {'deleting': 'OK'}
