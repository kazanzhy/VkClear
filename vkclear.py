#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import tkinter as tk
import vk_api

API_VERSION = '5.80'
APP_ID = '5206195'

BUTTON_STYLE = {
    'font': 'Tahoma 10',
    'bg': '#5B7FA6', 
    'fg': 'white',
}

LABEL_STYLE = {
    'fg': '#2B587A',
    'font': 'Verdana 14',
}

ENTRY_STYLE = {
    'width': 20,
    'font': 'Arial 12',
}


class MainWindow(tk.Tk):
    """ Класс отрисовки основного окна """

    def __init__(self, app_id='5206195'):
        super().__init__()
        self.title(u'VkClear v.0.1') # Название приложения
        self.resizable(False, False) # размер окна может быть изменён
        self.is_authorized = False
        self.app_id = app_id
        self.user_name = 'name'
        self.user_surname = 'surname'
        self.status = u'Введите логин и пароль'
        self.construct()
        # self.configure(background='grey') # Цвет фона
        # self.bind("<Enter>", self.submit)

    def construct(self):
        # Первая строка: Надписи к виджетам ввода информации и пробелов
        tk.Label(self, text=u"Логин:").grid(row=0, column=1, sticky='w')
        tk.Label(self, text=u"Пароль:").grid(row=0, column=3, sticky='w')
        tk.Label(self, text=u"app ID: " + self.app_id).grid(row=0, column=5, sticky='w')

        # Вторая строка: виджеты ввода информации
        self.login = tk.Entry(self, ENTRY_STYLE)
        self.login.grid(row=1, column=1, sticky='w')
        
        self.passwd = tk.Entry(self, ENTRY_STYLE, show='*')
        self.passwd.grid(row=1, column=3, sticky='w')
        
        self.subbut = tk.Button(self, BUTTON_STYLE, text=u"Войти!", command=self.submit)
        self.subbut.grid(row=1, column=5)

        # Третья строка: имя и фамилия пользователя
        tk.Label(self, LABEL_STYLE, text=self.user_name).grid(row=4, column=1, sticky='w')
        tk.Label(self, LABEL_STYLE, text=self.user_surname).grid(row=5, column=1, sticky='w')

        # Кнопки
        tk.Button(self, BUTTON_STYLE, text=u"Удалить все посты",
                  command=self.delete_wallposts).grid(row=7, column=1, sticky='w')
        tk.Button(self, BUTTON_STYLE, text=u"Удалить все фото",
                  command=self.delete_photos).grid(row=7, column=3, columnspan=3, sticky='e')
        tk.Button(self, BUTTON_STYLE, text=u"Удалить всех друзей",
                  command=self.delete_friends).grid(row=8, column=1, sticky='w')
        tk.Button(self, BUTTON_STYLE, text=u"Удалить все видео",
                  command=self.delete_videos).grid(row=8, column=3, columnspan=3, sticky='e')
        tk.Button(self, BUTTON_STYLE, text=u"Удалить все сообщения",
                  command=self.delete_messages).grid(row=9, column=1, sticky='w')
        tk.Button(self, BUTTON_STYLE, text=u"Удалить все аудио",
                  command=self.delete_audios).grid(row=9, column=3, columnspan=3, sticky='e')
        tk.Button(self, BUTTON_STYLE, text=u"Удалить все группы",
                  command=self.delete_groups).grid(row=10, column=1, sticky='w')
        tk.Button(self, BUTTON_STYLE, text=u"Удалить все закладки",
                  command=self.delete_bookmarks).grid(row=10, column=3, columnspan=3, sticky='e')
        tk.Button(self, BUTTON_STYLE, text=u"Удалить все мероприятия",
                  command=self.delete_events).grid(row=11, column=1, sticky='w')
        tk.Button(self, BUTTON_STYLE, text=u"Удалить все комментарии",
                  command=self.delete_comments).grid(row=11, column=3, columnspan=3, sticky='e')

        # отрисовывает статусбар
        self.draw_statusbar()

    def draw_statusbar(self):
        """
        Метод принимает сообщение для статусбара,
        отрисовывает его и обновляет GUI
        """

        # Последняя строка - строка состояния
        tk.Label(self, bg='yellow', fg='#2B587A', text=self.status).grid(row=13, column=1, columnspan=5, sticky='we')

        # Обновление всего GUI
        self.update()

    def confirm(self, message):
        """
        Вызывается для подтверждения удаления.
        Проверяет авторизацию и отрисовывает окно подтверждения.
        """

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
            tk.Button(self.confirmroot, BUTTON_STYLE, text=u"Да", command=accept).grid(row=3, column=1, sticky='w')
            tk.Button(self.confirmroot, BUTTON_STYLE, text=u"Нет", command=decline).grid(row=3, column=1, sticky='e')
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
        """
        Извлекаем логин и пароль в локальные переменные.
        Пытаемся аутентифицироваться.
        """

        login = self.login.get()
        passwd = self.passwd.get()
        if login and passwd:
            try:
                self.vk = vk_api.VkApi(login, passwd)
                self.vk.auth()
                self.vkapi = self.vk.get_api()
            except vk_api.AuthError:
                self.status = u"Неверный логин или пароль"
                self.draw_statusbar()
            else:
                # Сохраняем ответ в локальную переменную, а потом отрисовываем окно с новыми данными
                self.is_authorized = True
                user = self.vkapi.users.get()[0]
                self.user_name = user['first_name']
                self.user_surname = user['last_name']
                self.status = u"Аутентификация прошла успешно"
                self.construct()

    def delete_wallposts(self):
        # Первым запросом узнаем кол-во постов, а после проходимся по каждому и удаляем
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
                uid = self.vkapi.messages.getDialogs(offset=0, count=1)[1]['uid']
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
            count = self.vkapi.video.get()[0]
            print(count)
            for i in range(count):
                time.sleep(0.333)
                video_id = self.vkapi.video.get()[1]['vid']
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
                owner_id = all_audios[i]['owner_id']
                self.vkapi.audio.delete(audio_id=audio_id, owner_id=owner_id)
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

    def delete_comments(self):
        count_deleted_comments = 0

        def _delete_comment(owner_id, comment_id):
            nonlocal count_deleted_comments
            self.vkapi.wall.deleteComment(owner_id=owner_id, comment_id=comment_id)
            count_deleted_comments += 1

        def _find_posts_with_comment(count=100):
            """
            Метод нужен для получения списка id всех постов,
            в которых пользователь оставил комментарий.

            До тех пор, пока количество полученных постов равно @count,
            продолжать запрашивать данные.
            Иначе, задать флаг @loop в False чтобы остановить цикл запроса.
            """
            filtered_posts = []
            loop = True
            start_from = None

            while True and loop:
                response = self.vkapi.newsfeed.getComments(count=count, start_from=start_from)
                start_from = response.get('next_from')
                posts = response.get('items')
                if len(posts) < count:
                    loop = False
                for post in posts:
                    post_id = post.get('post_id')
                    source_id = post.get('source_id')
                    filtered_posts.append((source_id, post_id))
            return filtered_posts

        def _find_and_delete_comments_in_certain_post(source_id, post_id, count=100):
            offset = 0
            user_id = self.vkapi.users.get()[0].get('id')
            count_comments = -1
            try:
                count_comments = self.vkapi.wall.getComments(owner_id=source_id, post_id=post_id).get('count')
            except vk_api.ApiError:
                print('Something went wrong / https://vk.com/topic{}_{}?offset=400'.format(source_id, post_id, offset))

            while offset <= count_comments:
                try:
                    comments = self.vkapi.wall.getComments(count=count, owner_id=source_id, post_id=post_id, offset=offset).get('items')
                    offset += count
                    for comment in comments:
                        comment_author_id = comment.get('from_id')
                        if user_id == comment_author_id:
                            comment_id = comment.get('id')
                            _delete_comment(owner_id=source_id, comment_id=comment_id)
                except vk_api.ApiError:
                    print('Something went wrong / https://vk.com/topic{}_{}?offset=400'.format(source_id, post_id, offset))

        if self.confirm(' комментарии'):
            posts = _find_posts_with_comment()
            for post in posts:
                _find_and_delete_comments_in_certain_post(*post)
        self.status = u'Удалено всего комментариев: {}'.format(count_deleted_comments)
        self.draw_statusbar()


if __name__ == '__main__':
    MainWindow().mainloop()


