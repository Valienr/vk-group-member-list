import requests
import json
import time
import os
#import datetime
from win10toast import ToastNotifier


# анализирует и сверяет подписчиков группы до 1000 человека
def create_snapshot(data):
    """ создаём список участников группы"""
    with open(file, 'w') as f_obj:
        json.dump(current_users, f_obj)
        notif_text('Список обновлён', 'данные сохранены в {0}'.format(file))

# def backendprint(older_members):
#     print('Анализ подписчиков сообщества {0}.'.format(key.upper()))
#     print('участников ранее/сейчас: {0}/{1}'.format(len(older_members), len(current_users)))
#     print('выбыли {0}, добавились {1}'.format(result, result2))


def notif(add_or_lost, member, ico):
    toaster = ToastNotifier()
    for m in member:
        xlink = 'https://vk.com/id{0}'.format(m)
        toaster.show_toast(add_or_lost, "пользователь {0}".format(m), icon_path=ico, duration=10)
        print(xlink)


def notif_text(title, text):
    t = ToastNotifier()
    t.show_toast(title, text, icon_path=None, duration=10)


def update():
    notif_text('Обновите список', 'следующая проверка через {0} минут'.format(sleaptime))
    rewrite = input('обновить список? y/n')
    if rewrite == 'y':
        create_snapshot(current_users, result)
    else:
        pass

# указываем имя группы, и время в минутах
key = 'dobrybobrstudio' # id группы
sleaptime = 60  # время в минутах

j = requests.get('https://api.vk.com/method/groups.getMembers?group_id=' + key).json()
current_users = j['response']['users']
file = 'old_{0}.json'.format(key)


def run():
    print(time.strftime('%X'))
    try:
        with open(file) as f:
            older_members = json.load(f)
    except FileNotFoundError:
        print("Файл '{0}' не был найден. \nСоздан новый от {1}".format(file, time.strftime('%Y.%m.%d.')))
        #create_snapshot(current_users, result)

    else:
        result = list(set(older_members) - set(current_users))
        result2 = list(set(current_users) - set(older_members))
        #  backendprint(older_members)
        print('Анализ подписчиков сообщества {0}.'.format(key.upper()))
        print('участников ранее/сейчас: {0}/{1}'.format(len(older_members), len(current_users)))
        print('выбыли {0}, добавились {1}'.format(result, result2))
        if len(result2) > 0:
            notif("В группу вступил", result2, 'happy.ico')
            if len(result) > 0:
                notif("Группу покинул", result, 'sad.ico')
            update()
        else:
            pass
    time.sleep(sleaptime * 60)
    pass



notif_text("Мониторинг группы {0}".format(key),
           "В группе {} человек.\nПроверка каждые {} минут".format(len(current_users), sleaptime))
while True:
    run()

