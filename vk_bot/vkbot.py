from vk_bot.vk_config import GROUP_ID, TOKEN
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from vk_bot.db_session import *
from vk_bot.__all_models import BugReport, Comment
import datetime
from vk_bot.vacancies import get_vacancies, ServerError


def main():
    global_init("feedback/feedback.sqlite")
    vk_session = vk_api.VkApi(
        token=TOKEN)
    vk = vk_session.get_api()

    longpoll = VkBotLongPoll(vk_session, GROUP_ID)
    bot_state = {}

    def send_msg(msg):
        vk.messages.send(user_id=event.obj.message['from_id'],
                         message=msg,
                         random_id=random.randint(0, 2 ** 64))

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.obj.message['from_id'] in bot_state and bot_state[event.obj.message['from_id']]:
                state = bot_state[event.obj.message['from_id']]
                if state == 1:
                    send_msg('Спасибо, ваше мнение для нас очень важно.')
                    Comment().new(event.obj.message['from_id'], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                  event.obj.message['text'])
                    bot_state[event.obj.message['from_id']] = 0
                elif state == 2:
                    BugReport().new(event.obj.message['from_id'], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                    event.obj.message['text'])
                    send_msg('Спасибо за ваш отзыв, мы постараемся исправить проблему в ближайшем будущем.')
                    bot_state[event.obj.message['from_id']] = 0
                elif state == 4:
                    parameters = [r.strip() for r in event.obj.message['text'].split(',')]
                    try:
                        vacancies = get_vacancies(parameters[0], parameters[1])
                    except ServerError:
                        send_msg('Не удалось получить ответ от сервера, попробуйте позже')
                        bot_state[event.obj.message['from_id']] = 0
                    except Exception:
                        send_msg('Данные введены некорректно, попробуйте заново.')
                        send_msg('Формат: <должность>, <мин. зарплата>')
                    else:
                        if len(vacancies) == 0:
                            send_msg('По данным критериям ничего не найдено')
                        else:
                            vacancy_list = [f"{i}) {v['title']}, {v['salary']}" for i, v in enumerate(vacancies)]
                            send_msg('\n'.join(vacancy_list))

                if bot_state[event.obj.message['from_id']] == 0:
                    send_msg('1 - написать отзыв или предложение\n 2 - сообщить о неправильной работе сайта\n 3 - документация к api\n 4 - посмотреть список доступных вакансий\n иначе напишите сообщение и модератор вскоре на него ответит')

            elif event.obj.message['from_id'] not in bot_state:
                send_msg('1 - написать отзыв или предложение\n 2 - сообщить о неправильной работе сайта\n 3 - документация к api\n 4 - посмотреть список доступных вакансий\n иначе напишите сообщение и модератор вскоре на него ответит')
                bot_state[event.obj.message['from_id']] = 0
            else:
                key = event.obj.message['text'][0]
                if key == '1':
                    send_msg('Пожалуйста, поделитесь вашим мнением по поводу сайта.')
                    bot_state[event.obj.message['from_id']] = 1
                elif key == '2':
                    send_msg('Пожалуйста, максимально подробно опишите вашу проблему.')
                    bot_state[event.obj.message['from_id']] = 2
                elif key == '3':
                    send_msg('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
                elif key == '4':
                    send_msg('Введите название должности и минимальную желаемую зарплату по образцу:<должность>, <мин. зарплата>')
                    bot_state[event.obj.message['from_id']] = 4
                else:
                    send_msg('Модератор вам скоро ответит, пожалуйста подождите.')


if __name__ == '__main__':
    main()
