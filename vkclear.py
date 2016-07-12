#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
import tkinter as tk
import vk


class MainWindow():
    '''
    Класс отрисовки основного окна
    '''
    def __init__(self, root, app_id='5206195'):
        self.root = root
        self.root.title(u'VkClear v.0.1') # Название приложения
        self.root.geometry('590x375') # ширина=500, высота=500
        #self.root.configure(background='grey') # Цвет фона
        self.root.resizable(False, False) # размер окна может быть изменён
        #self.root.bind("<Enter>", self.submit)
        self.is_authorized = False
        self.app_id = app_id
        self.username = 'name'
        self.usersurname = 'surname'
        self.status = u'Введите логин и пароль'
        self.construct()

    def construct(self):
        # Добавляем пропуски между столбцами
        tk.Label(self.root, text='    ').grid(row=0, column=0, rowspan=13)
        tk.Label(self.root, text='    ').grid(row=0, column=2, rowspan=13)
        tk.Label(self.root, text='    ').grid(row=0, column=4, rowspan=13)

        # Первая строка: Надписи к виджетам ввода информации и пробелов
        tk.Label(self.root, text=u"Логин:").grid(row=0, column=1, sticky='w')
        tk.Label(self.root, text=u"Пароль:").grid(row=0, column=3, sticky='w')
        tk.Label(self.root, text=u"app ID: " + self.app_id).grid(row=0, column=5, sticky='w')

        # Вторая строка: виджеты ввода информации
        self.login = tk.Entry(self.root, width=20, font='Arial 12')
        self.login.grid(row=1, column=1, sticky='w')
        self.passwd = tk.Entry(self.root, width=20, font='Arial 12', show='*')
        self.passwd.grid(row=1, column=3, sticky='w')
        self.subbut = tk.Button(self.root, font='tahoma 8', bg='#5B7FA6', fg='white', text=u"Войти!", command=self.submit)
        self.subbut.grid(row=1, column=5)

        # Третья строка: имя и фамилия пользователя
        tk.Label(self.root, text='    ').grid(row=2, column=1)
        tk.Label(self.root, text='    ').grid(row=3, column=1)
        tk.Label(self.root, text=self.username, fg='#2B587A', font='verdana 14').grid(row=4, column=1, sticky='w')
        tk.Label(self.root, text=self.usersurname, fg='#2B587A', font='verdana 14').grid(row=5, column=1, sticky='w')

        # Кнопки
        tk.Label(self.root, text='    ').grid(row=6, column=1)
        tk.Button(self.root, font='tahoma 10', bg='#5B7FA6', fg='white', text=u"Удалить все посты",
                  command=self.delete_wallposts).grid(row=7, column=1, sticky='w')
        tk.Button(self.root, font='tahoma 10', bg='#5B7FA6', fg='white', text=u"Удалить все фото",
                  command=self.delete_photos).grid(row=7, column=3, columnspan=3, sticky='e')
        tk.Button(self.root, font='tahoma 10', bg='#5B7FA6', fg='white', text=u"Удалить всех друзей",
                  command=self.delete_friends).grid(row=8, column=1, sticky='w')
        tk.Button(self.root, font='tahoma 10', bg='#5B7FA6', fg='white', text=u"Удалить все видео",
                  command=self.delete_videos).grid(row=8, column=3, columnspan=3, sticky='e')
        tk.Button(self.root, font='tahoma 10', bg='#5B7FA6', fg='white', text=u"Удалить все сообщения",
                  command=self.delete_messages).grid(row=9, column=1, sticky='w')
        tk.Button(self.root, font='tahoma 10', bg='#5B7FA6', fg='white', text=u"Удалить все аудио",
                  command=self.delete_audios).grid(row=9, column=3, columnspan=3, sticky='e')
        tk.Button(self.root, font='tahoma 10', bg='#5B7FA6', fg='white', text=u"Удалить все группы",
                  command=self.delete_groups).grid(row=10, column=1, sticky='w')
        tk.Button(self.root, font='tahoma 10', bg='#5B7FA6', fg='white', text=u"Удалить все закладки",
                  command=self.delete_bookmarks).grid(row=10, column=3, columnspan=3, sticky='e')
        tk.Button(self.root, font='tahoma 10', bg='#5B7FA6', fg='white', text=u"Удалить все мероприятия",
                  command=self.delete_events).grid(row=11, column=1, sticky='w')
        tk.Button(self.root, font='tahoma 10', bg='#5B7FA6', fg='white', text=u"Удалить всю страницу",
                  command=self.delete_account).grid(row=11, column=3, columnspan=3, sticky='e')

        # отрисовывает статусбар
        self.draw_statusbar()

    def draw_statusbar(self):
        # Метод принимает сообщение для статусбара отрисовывает его и обновляет GUI
        # Последняя строка: строка состояния
        tk.Label(self.root, text='    ').grid(row=12, column=4)
        tk.Label(self.root, bg='yellow', fg='#2B587A', text=self.status).grid(row=13, column=1, columnspan=5, sticky='we')
        # Обновление всего GUI
        self.root.update()

    def confirm(self, message):
        # Вызывается для подтверждения удаления. Проверяет авторизацию и отрисовывает окно подтверждения
        def accept():
            # Функция вызывается если пользователь нажал кнопку "Да"
            self.confirmed = True
            self.confirmroot.destroy()

        def decline():
            # Функция вызывается если пользователь нажал кнопку "Нет" или закрыл окно
            self.confirmed = False
            self.confirmroot.destroy()

        def create_confirm_window():
            self.confirmroot = tk.Toplevel()
            self.confirmroot.title(u'Подтвердите выбор') # Название приложения
            self.confirmroot.geometry('410x110') # ширина=200, высота=100
            self.confirmroot.resizable(False, False) # размер окна может быть изменён
            self.confirmroot.protocol('WM_DELETE_WINDOW', decline) # обработчик закрытия окна
            tk.Label(self.confirmroot, text='    ').grid(row=0, column=0, columnspan=5)
            tk.Label(self.confirmroot, text='    ').grid(row=0, column=3, columnspan=5)
            tk.Label(self.confirmroot, text=u'Вы действительно хотите удалить все{}?'.format(message), fg='#2B587A', font='tahoma 10').grid(row=1, column=1)
            tk.Label(self.confirmroot, text='    ').grid(row=2, column=0)
            tk.Button(self.confirmroot, font='tahoma 10', bg='#5B7FA6', fg='white', text=u"Да", command=accept).grid(row=3, column=1, sticky='w')
            tk.Button(self.confirmroot, font='tahoma 10', bg='#5B7FA6', fg='white', text=u"Нет", command=decline).grid(row=3, column=1, sticky='e')
            tk.Label(self.confirmroot, text='    ').grid(row=4, column=0)
            self.confirmroot.wait_window()

        self.confirmed = False
        if not self.is_authorized:
            self.status = u'Прежде авторизуйтесь!'
            self.draw_statusbar()
            return False
        else:
            create_confirm_window()
            return self.confirmed

    def submit(self):
        # Извлекаем логин и пароль в локальные переменные и пытаемся аутентифицироваться
        scope = 'friends, photos, audio, video, wall, groups, messages'
        login = tk.Entry.get(self.login)
        passwd = tk.Entry.get(self.passwd)
        if login != '' and passwd != '':
            try:
                self.session = vk.AuthSession(app_id=self.app_id, user_login=login, user_password=passwd, scope=scope)
                self.vkapi = vk.API(self.session, api_version='5.52')
            except:
                self.status = u"Неверный логин или пароль"
                self.draw_statusbar()
            else:
                # Сохраняем ответ в локальную переменную, а потом отрисовываем окно с новыми данными
                self.is_authorized = True
                user = self.vkapi.users.get()[0]
                self.username = user['first_name']
                self.usersurname = user['last_name']
                self.status = u"Аутентификация прошла успешно"
                self.construct()

    def delete_wallposts(self):
        # Первым запросом узноаум кол-во постов, а после проходимся по каждому и удаляем
        if self.confirm(' посты'):
            count = self.vkapi.wall.get(count=1)[0]
            for i in range(count):
                time.sleep(0.333)
                post_id = self.vkapi.wall.get(offset=0, count=1)[1]['id']
                time.sleep(0.333)
                self.vkapi.wall.delete(post_id=post_id)
                self.status = u'Удалено постов со стенки: {0}/{1}'.format(i+1, count)
                self.draw_statusbar()

    def delete_friends(self):
        # Загружаем идентификаторы всех друзей и в цикле удаляем каждого
        if self.confirm('х друзей'):
            friends_ids = self.vkapi.friends.get()
            count = len(friends_ids)
            for i in range(count):
                time.sleep(0.333)
                self.vkapi.friends.delete(user_id=friends_ids[i])
                self.status = u'Удалено друзей: {0}/{1}'.format(i+1, count)
                self.draw_statusbar()

    def delete_messages(self):
        # Удаляет все диалоги
        if self.confirm(' диалоги'):
            #
            count = self.vkapi.messages.getDialogs(count=1)[0]
            for i in range(count):
                time.sleep(0.333)
                uid = self.vkapi.messages.getDialogs(offset=i, count=1)[1]['uid']
                time.sleep(0.333)
                self.vkapi.messages.deleteDialog(user_id=uid)
                self.status = u'Удалено диалогов: {0}/{1}'.format(i+1, count)
                self.draw_statusbar()

    def delete_groups(self):
        # Узнаем количество групп и пабликов, а потом достаем идентификатор каждого и покидаем его
        if self.confirm(' группы'):
            count = self.vkapi.groups.get(count=1, filter='groups, publics')[0]
            for i in range(count):
                time.sleep(0.333)
                current_id = self.vkapi.groups.get(count=1, offset=0, filter='groups, publics')[1]
                time.sleep(0.333)
                self.vkapi.groups.leave(group_id=current_id)
                self.status = u'Удалено групп и пабликов: {0}/{1}'.format(i+1, count)
                self.draw_statusbar()

    def delete_events(self):
        # Узнаем количество ивентов, а потом достаем идентификатор каждого и покидаем его
        if self.confirm(' ивенты'):
            count = self.vkapi.groups.get(count=1, filter='events')[0]
            for i in range(count):
                time.sleep(0.333)
                current_id = self.vkapi.groups.get(count=1, offset=0, filter='events')[1]
                time.sleep(0.333)
                self.vkapi.groups.leave(group_id=current_id)
                self.status = u'Удалено мероприятий: {0}/{1}'.format(i+1, count)
                self.draw_statusbar()

    def delete_photos(self):
        # Удаляет все фотографии.
        # Фото, добавленное пользователем - поальбомно, а фото сохраненные, профиля и стенки - поэлементно
        if self.confirm(' фото'):
            # Достаем id всех альбомов пользователя и удаляем их
            time.sleep(0.333)
            albums = self.vkapi.photos.getAlbums()
            count = len(albums)
            for i in range(count):
                aid = albums[i]['aid']
                self.vkapi.photos.deleteAlbum (album_id=aid)
                self.status = u'Удалено альбомов: {0}/{1}'.format(i+1, count)
                self.draw_statusbar()
            # Достаем все фотки из альбомов 'wall', 'profile', 'saved'
            photos = []
            for aid in ['wall', 'profile', 'saved']:
                time.sleep(0.333)
                photos.extend(self.vkapi.photos.get(album_id=aid, count=1000))
            # Удаляем все фотографии
            count = len(photos)
            for i in range(count):
                photo_id = photos[i]['pid']
                time.sleep(0.333)
                self.vkapi.photos.delete(photo_id=photo_id)
                self.status = u'Удалено фотографий: {0}/{1}'.format(i+1, count)
                self.draw_statusbar()

    def delete_videos(self):
        if self.confirm(' видео'):
            count = self.vkapi.video.get(count=1)[0]
            for i in range(count):
                time.sleep(0.333)
                video_id = self.vkapi.video.get(count=1, offset=0)[1]['vid']
                time.sleep(0.333)
                self.vkapi.video.delete(video_id=video_id)
                self.status = u'Удалено видео: {0}/{1}'.format(i+1, count)
                self.draw_statusbar()

    def delete_audios(self):
        # Запрашивает инфу о всех аудио и удаляем их. Если их больше 6000, то повторяем
        if self.confirm(' аудио'):
            all_audios = self.vkapi.audio.get()
            count = len(all_audios)
            for i in range(count):
                time.sleep(0.333)
                audio_id = all_audios[i]['aid']
                self.vkapi.audio.delete(audio_id=audio_id)
                self.status = u'Удалено аудиозаписей: {0}/{1}'.format(i+1, count)
                self.draw_statusbar()
            # Если аудиозаписей больше 6000, то придется удалять за несколько подходов
            if count == 6000:
                self.delete_audios()

    def delete_bookmarks(self):
        # Удаляет всех пользователей и ссылки, добавленных в закладки
        if self.confirm(' закладки'):
            count = self.vkapi.fave.getUsers()[0]
            for i in range(count):
                time.sleep(0.333)
                user_id = self.vkapi.fave.getUsers(count=1, offset=0)[1]['uid']
                time.sleep(0.333)
                self.vkapi.fave.removeUser(user_id=user_id)
                self.status = u'Удалено пользователей из закладок: {0}/{1}'.format(i+1, count)
                self.draw_statusbar()
            count = self.vkapi.fave.getLinks()[0]
            for i in range(count):
                time.sleep(0.333)
                link_id = self.vkapi.fave.getLinks(count=1, offset=0)[1]['id']
                time.sleep(0.333)
                self.vkapi.fave.removeLink(link_id=link_id)
                self.status = u'Удалено ссылок из закладок: {0}/{1}'.format(i+1, count)
                self.draw_statusbar()

    def delete_account(self):
        # Пока эта опция не работает
        self.status = u'Эта опция пока не работает'
        self.draw_statusbar()


# Номер приложения в ВК, с помощью которого происходит взаимодействие с VK API
# Можете указать свое приложение с необходимыми правами доступа (https://vk.com/apps?act=manage)
app_id = '5206195'

root = tk.Tk()
mainw = MainWindow(root, app_id = app_id)
root.mainloop()



