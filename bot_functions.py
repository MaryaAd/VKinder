from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from db_functions import add_user, add_user_profile, add_photo, check_db_favorites, check_db_black
from vk_info_user import search_users, get_photo, sort_photo, get_info_users
from settings import KEY_GROUP
from keyboard import *


def get_long_poll(token):
    """Gets a token for interacting with the server."""
    vk = vk_api.VkApi(token=token)
    longpoll = VkLongPoll(vk)
    return longpoll


def loop_bot():
    """Gets the user id and message text."""
    for event in get_long_poll(KEY_GROUP).listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                message_text = event.text.lower()
                return message_text, event.user_id


def menu_bot(id_num):
    """Bot's response."""
    write_msg(id_num,
              f'\nВас приветствует бот - Vkinder!\n'
              f'Вам одиноко?\n'
              f' Хотите найти пару?\n'
              f'Или надумали познакомиться с избранными?\n',
              keyboard=main_keyboard)


def menu_bot_2(id_num):
    """Bot's response."""
    write_msg(id_num,
              f'\nДля поиска введите пол, границы возраста и город\n'
              f'Например, девушка 18-25 Москва\n'
              f'Перейти в изранное - 1\n'
              f'Перейти в черный список - 0\n',
              keyboard=next_keyboard)


def menu_bot_3(id_num):
    """Bot's response."""
    write_msg(id_num,
              f'\nЭто была последняя анкета.\n'
              f'Для выхода в основное меню нажмите кнопку\n',
              keyboard=start_keyboard)


def write_msg(user_id, message, attachment=None, keyboard=None):
    post = {'user_id': user_id,
            'message': message,
            'attachment': attachment,
            'random_id': randrange(10 ** 7)
            }
    if keyboard != None:
        post['keyboard'] = keyboard.get_keyboard()
    else:
        post = post

    vk_api.VkApi(token=KEY_GROUP).method('messages.send', post)


def menu():
    """Interacts with the bot."""
    while True:
        msg_text, user_id = loop_bot()
        if msg_text == 'привет':
            menu_bot(user_id)
            msg_text, user_id = loop_bot()
            if msg_text.lower() == 'да':
                add_user(user_id)
                menu_bot_2(user_id)
                msg_text, user_id = loop_bot()
                if len(msg_text) > 1:
                    sex = 0
                    if msg_text.split()[0].lower() in ['женщина', 'девушка']:
                        sex = 1
                    elif msg_text.split()[0].lower() in ['мужчина', 'парень']:
                        sex = 2
                    age_from = msg_text.split()[1][0:2]
                    if int(age_from) < 18:
                        write_msg(user_id, 'Минимальный возраст - 18 лет.')
                        age_from = 18
                    age_to = msg_text.split()[1][3:]
                    if int(age_to) >= 100:
                        write_msg(user_id, 'Максимальный возраст 99 лет.')
                        age_to = 99
                    city = msg_text.split()[2].lower()
                    result = search_users(sex, int(age_from), int(age_to), city)
                    for item in result:
                        user_photo = get_photo(item[3])
                        sorted_user_photo = sort_photo(user_photo)
                        write_msg(user_id, f'\n{item[0]}  {item[1]}   {item[2]}')
                        if len(sorted_user_photo) == 3:
                            write_msg(user_id,
                                      f'фото: ',
                                      attachment=','.join([
                                          'photo{}_{}'.format(sorted_user_photo[-1][1], sorted_user_photo[-1][3]),
                                          'photo{}_{}'.format(sorted_user_photo[-2][1], sorted_user_photo[-2][3]),
                                          'photo{}_{}'.format(sorted_user_photo[-3][1], sorted_user_photo[-3][3])]))
                        else:
                            for photo in range(len(sorted_user_photo)):
                                write_msg(user_id,
                                          f'фото: ',
                                          attachment=
                                          f'photo{sorted_user_photo[photo][1]}_{sorted_user_photo[photo][3]}')
                        write_msg(user_id, 'Выберите действие:', keyboard=find_keyboard)
                        msg_text, user_id = loop_bot()
                        if msg_text.lower() == 'далее':
                            if len(item) >= len(result) - 1:
                                menu_bot_3(user_id)
                        elif msg_text.lower() == 'добавить':
                            user_profile = get_info_users(item[3])
                            add_user_profile(user_profile, user_id, 1)
                            if sorted_user_photo == ['нет фото']:
                                pass
                            else:
                                add_photo(item[3])
                        elif msg_text.lower() == 'заблокировать':
                            user_profile = get_info_users(item[3])
                            add_user_profile(user_profile, user_id, 0)
                        elif msg_text.lower() == 'выход':
                            write_msg(user_id, 'Для активации бота нажмите кнопку', keyboard=start_keyboard)
                            break
                elif msg_text == '1':
                    profile = check_db_favorites(user_id)
                    write_msg(user_id, 'Анкеты избранного: ')
                    for i in profile:
                        write_msg(user_id, f'{i.first_name} {i.last_name}, {i.link}')
                    write_msg(user_id, 'Для выхода в основное меню нажмите кнопку', keyboard=start_keyboard)
                elif msg_text == '0':
                    profile = check_db_black(user_id)
                    write_msg(user_id, 'Анкеты черного списка: ')
                    for i in profile:
                        write_msg(user_id, f'{i.first_name} {i.last_name}, {i.link}')
                    write_msg(user_id, 'Для выхода в основное меню нажмите кнопку', keyboard=start_keyboard)
            else:
                write_msg(user_id,
                          f"\nОчень жаль. До свидания.")
                break
        else:
            write_msg(user_id,
                      f"\nДля активации бота нажмите кнопку",
                      keyboard=start_keyboard)
