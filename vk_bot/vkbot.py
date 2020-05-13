from typing import NoReturn
from vk_bot.mess_templates import info, feedback, bug_report, api_docs, vacancy_filter, else_res
from vk_bot.vk_config import GROUP_ID, TOKEN
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from vk_bot.db_session import *
from vk_bot.__all_models import BugReport, Comment
import datetime
from vk_bot.vacancies import get_vacancies, ServerError


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
        if event.obj.message['from_id'] in self.__bot_state and self.__bot_state[event.obj.message['from_id']]:
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
            "4": (4, vacancy_filter),
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
        Comment().new(recipient, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), usr_mess)
        self.__bot_state[recipient] = 0

    def __end_bug_report_dialog(self, recipient: int, usr_mess: str) -> None:
        self._send_mess(recipient, 'Спасибо за ваш отзыв, мы постараемся исправить проблему в ближайшем будущем.')
        BugReport().new(recipient, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        usr_mess)
        self.__bot_state[recipient] = 0

    def __get_vacancies(self, recipient: int, usr_mess: str) -> None:
        parameters = [r.strip() for r in usr_mess.split(',')]
        try:
            vacancies = get_vacancies(parameters[0], parameters[1])
        except ServerError:
            self._send_mess(recipient, 'Не удалось получить ответ от сервера, попробуйте позже')
            self.__bot_state[recipient] = 0
            return
        except Exception:
            self._send_mess(recipient, 'Данные введены некорректно, попробуйте заново.')
            self._send_mess(recipient, 'Формат: <должность>, <мин. зарплата>')
            return
        if len(vacancies) == 0:
            self._send_mess(recipient, 'По данным критериям ничего не найдено')
        else:
            vacancy_list = [f"{i}) {v['title']}, {v['salary']}" for i, v in enumerate(vacancies)]
            self._send_mess(recipient, '\n'.join(vacancy_list))

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
    global_init("feedback/feedback.sqlite")
    bot = GroupBot(TOKEN, GROUP_ID)
    bot.loop()
