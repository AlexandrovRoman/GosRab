import requests
from vk_bot.vk_config import EMAIL, PASSWORD


class CustomError(Exception):
    pass


class MinSalTypeError(CustomError):
    def __init__(self):
        super().__init__('Минимальная зарплата должна быть числом')


class ServerError(CustomError):
    def __init__(self):
        super().__init__('Не удалось получить ответ от сервера, повторите попытку позже.')


class AuthorizationError(CustomError):
    def __init__(self):
        super().__init__('Адрес почты или пароль введены некорректно')


class CriterionError(CustomError):
    def __init__(self):
        super().__init__('Название должности или желаемая зарплата введены некорректно')


class FormatError(CustomError):
    def __init__(self, format_, filter_):
        super().__init__(f'Некорректный параметр для формата или фильтрации: {format_}, {filter_}')


class UserApiSession:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.session = requests.Session()
        self._auth()

    def _auth(self):
        response = self.session.get(f"https://pfproject.herokuapp.com/api/login/{self.email}/{self.password}").json()
        if response.get('error', False):
            raise AuthorizationError()
        else:
            print(response)
            print('Authorization completed')

    def _get_vacancies(self):
        response = self.session.get('https://pfproject.herokuapp.com/api/vacancy')
        if not response:
            raise ServerError()
        json_resp = response.json()
        if json_resp.get('error', 0):
            raise AuthorizationError()
        return json_resp['vacancy']

    @staticmethod
    def _f_vacancies(vacancies, format_, acceptable_vacancies, filter_):
        if format_ not in (list, dict):
            raise FormatError(format_, filter_)
        return (vacancies if format_ == dict else acceptable_vacancies
                if filter_ not in ('sal', 'alph') else
                sorted(acceptable_vacancies,
                       key=lambda x: x['salary' if filter_ == 'sal' else 'title'],
                       reverse=filter_ == 'sal'))

    # возможные значения параметра format - 'json', 'list'
    # возможные значения параметра filter - 'sal', 'alph'(работает только при format == 'list'
    def get_vacancies(self, name='', min_salary=0, format_: object = dict, filter_='sal'):
        print(name, min_salary, format_, filter)

        vacancies = self._get_vacancies()
        acceptable_vacancies = filter(lambda vac: name.lower() in vac['title'].lower() and vac['salary'] > min_salary,
                                      vacancies)

        return self._f_vacancies(vacancies, format_, acceptable_vacancies, filter_)


if __name__ == '__main__':
    api = UserApiSession(EMAIL, PASSWORD)
    print('\n'.join(api.get_vacancies(min_salary=15000, name='', format_=list, filter_='sal')))
