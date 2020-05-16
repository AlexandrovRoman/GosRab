from typing import NoReturn
from vk_bot.mess_templates import info, feedback, bug_report, api_docs, vacancy_filter, else_res
from vk_bot.vk_config import GROUP_ID, TOKEN, EMAIL, PASSWORD, DB_USER, DB_URL, DB_NAME, DB_PASSWORD
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from vk_bot.db_session import *
from vk_bot.__all_models import BugReport, Comment
from vk_bot.api_interaction import UserApiSession, ServerError, CustomError, InputFormatError
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


class GroupBot:
    def __init__(self, token: str, group_id: int) -> None:
        vk_session = vk_api.VkApi(token=token)
        self.__vk = vk_session.get_api()
        self.__longpoll = VkBotLongPoll(vk_session, group_id)
        self.__bot_state = {}

    def _send_mess(self, recipient: int, mess: str) -> None:
        self.__vk.messages.send(user_id=recipient,
                                message=mess,
                                random_id=random.randint(0, 2 ** 64))

    def _new_mess_event(self, event) -> None:
        print(self.__bot_state)
        if self.__bot_state.get(event.obj.message['from_id'], False):
            self.__has_story(event.obj.message['from_id'], event.obj.message['text'])
        elif event.obj.message['from_id'] not in self.__bot_state:
            self.__has_not_story(event.obj.message['from_id'])
        else:
            self.__new_user(event.obj.message['from_id'], event.obj.message['text'][0])

    def __has_not_story(self, recipient: int) -> None:
        self._send_mess(recipient, info)
        self.__bot_state[recipient] = 0

    def __new_user(self, recipient: int, key: str) -> None:
        events = {
            "1": (1, feedback),
            "2": (2, bug_report),
            "3": (None, api_docs),
            "4": (3, vacancy_filter),
        }
        try:
            state, mess = events[key]
            self._send_mess(recipient, mess)
            if isinstance(state, int):
                self.__bot_state[recipient] = state
        except KeyError:
            self._send_mess(recipient, else_res)

    def __end_feedback_dialog(self, recipient: int, usr_mess: str) -> None:
        self._send_mess(recipient, 'Спасибо, ваше мнение для нас очень важно.')
        Comment().new(recipient, usr_mess)
        self.__bot_state[recipient] = 0

    def __end_bug_report_dialog(self, recipient: int, usr_mess: str) -> None:
        self._send_mess(recipient, 'Спасибо за ваш отзыв, мы постараемся исправить проблему в ближайшем будущем.')
        BugReport().new(recipient, usr_mess)
        self.__bot_state[recipient] = 0

    def __send_error_messages(self, recipient: int, ex: Exception) -> None:
        self._send_mess(recipient, str(ex))

    def __reset_state(self, recipient: int) -> None:
        self.__bot_state[recipient] = 0

    def __get_vacancies(self, recipient: int, usr_mess: str) -> None:
        try:
            self.__unsafe_get_vacancies(recipient, usr_mess)
        except ServerError as e:
            self.__send_error_messages(recipient, e)
            self.__reset_state(recipient)
        except CustomError as e:
            self.__send_error_messages(recipient, e)
            self._send_mess(recipient, 'Формат: <должность>, <мин. зарплата>')

    def __unsafe_get_vacancies(self, recipient: int, usr_mess: str) -> None:
        api = UserApiSession(EMAIL, PASSWORD)
        self.__check_input_format(usr_mess)
        name, min_salary, *_ = [r.strip() for r in usr_mess.split(',')]
        vacancy_list = [f"{i + 1}) {v['title']}, {v['salary']}"
                        for i, v in enumerate(api.get_vacancies(name, int(min_salary), format_=list, filter_='sal'))]
        self._send_mess(recipient, '\n'.join(vacancy_list) or "По данным критериям ничего не найдено")
        self.__bot_state[recipient] = 0

    def __check_input_format(self, msg):
        try:
            name, min_salary, *_ = [r.strip() for r in msg.split(',')]
            assert not min_salary.isdigit()
        except Exception:
            raise InputFormatError()

    def __send_default_mess(self, recipient: int, _=None) -> None:
        self._send_mess(recipient, info)

    def __has_story(self, recipient: int, usr_mess: str) -> None:
        events = [self.__send_default_mess, self.__end_feedback_dialog,
                  self.__end_bug_report_dialog, self.__get_vacancies]
        state = self.__bot_state[recipient]
        try:
            events[state](recipient, usr_mess)
        except IndexError:
            self.__send_default_mess(recipient)

    def loop(self) -> NoReturn:
        handlers = {
            VkBotEventType.MESSAGE_NEW: self._new_mess_event
        }
        for event in self.__longpoll.listen():
            try:
                handlers[event.type](event)
            except KeyError:
                print(f"Событие {event.type} не поддерживается")


if __name__ == '__main__':
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
    global_init(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_URL}/{DB_NAME}')
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    bot = GroupBot(TOKEN, GROUP_ID)
    bot.loop()
