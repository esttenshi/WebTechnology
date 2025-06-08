from application import app
from flask import render_template, session
from flask_restful import Resource
from Services.clubService import ClubService
from Services.userService import UserService
from Services.newsService import NewsService
from Services.userService import UserService
from Services.applicationService import ApplicationService
from Services.clubApplicationService import ClubApplicationService
from Services.eventService import EventService
import datetime

_clubService = ClubService()
_userService = UserService()
_newsService = NewsService()
_applicationService = ApplicationService()
_clubApplicationService = ClubApplicationService()
_eventService = EventService()

class PageController(Resource):

    """
    Класс контроллера для страниц
    
    ...
    
    Атрибуты
    -------
    _clubService : ClubService
        Сервис для работы с клубами
    _userService: UserService
        Сервис для работы с пользователями
    _newsService: NewsService
        Сервис для работы с новостями
        
    Методы
    ------
    get_page()
        Возвращает главную страницу
    get_main_page()
        Возвращает главную страницу
    get_entry_page()
        Возвращает страницу входа
    get_news_page()
        Возвращает страницу новостей
    get_clubs_page()
        Возвращает страницу клубов
    get_club_page(id)
        Возвращает страницу клуба
    get_applicationForm_page()
        Возвращает страницу формы заявки
    """

    @staticmethod
    @app.route('/', methods=['GET'])
    def get_page():

        """
        Возвращает главную страницу

        Возвращает
        ---------
        clubs : list
            Список всех клубов
        users : list
            Список всех пользователей
        news : list
            Список всех новостей
        """

        foundClubs = _clubService.findAllClubs()
        foundUsers = _userService.findAllUsers()
        foundNews = _newsService.findAllNews()
        return render_template('main.html', clubs=foundClubs, users=foundUsers, news=foundNews)

    @staticmethod
    @app.route('/main.html', methods=['GET'])
    def get_main_page():

        """
        Возвращает главную страницу
        
        Возвращает
        ---------
        clubs : list
            Список всех клубов
        users : list
            Список всех пользователей
        news : list
            Список всех новостей
        """

        foundClubs = _clubService.findAllClubs()
        foundUsers = _userService.findAllUsers()
        foundNews = _newsService.findAllNews()
        return render_template('main.html', clubs=foundClubs, users=foundUsers, news=foundNews)

    @staticmethod
    @app.route('/entry.html', methods=['GET'])
    def get_entry_page():
        """
        Возвращает страницу входа

        Возвращает
        ---------
        entry : html
            Страница входа
        """
        if session.get('user_logged'):
            user_id = session.get('user_id')  # предполагаем, что ID пользователя хранится в сессии
            if session.get('user_status') == 0:
                applications = _clubApplicationService.findAllClubApplications()
                users = _userService.findAllUsers()
                return render_template('admin_panel.html', applications = applications, users = users)
            else:
                if user_id:
                    user = _userService.findUser(int(user_id))
                    if user:
                        user_dict = {
                            "id": user.id,  # Передаем ID пользователя в шаблон
                            "surname": user.surname,
                            "name": user.name,
                            "patronymic": user.patronymic,
                            "status": user.status,
                            "clubs": user.clubs
                        }
                        return render_template('personal_account.html', user=user_dict)
                    else:
                        return render_template('personal_account.html', error="Данные пользователя не найдены", user=user)
                else:
                    return render_template('personal_account.html', error='ID пользователя не был найден')
        else:
            return render_template('entry.html')

    @staticmethod
    @app.route('/news.html', methods=['GET'])
    def get_news_page():

        """
        Возвращает страницу новостей
        
        Возвращает
        ---------
        clubs : list
            Список всех клубов
        news : list
            Список всех новостей
        """

        foundClubs = _clubService.findAllClubs()
        foundNews = _newsService.findAllNews()
        return render_template('news.html', clubs=foundClubs, news=foundNews)

    @staticmethod
    @app.route('/clubs.html', methods=['GET'])
    def get_clubs_page():

        """
        Возвращает страницу клубов
        
        Возвращает
        ---------
        clubs : list
            Список всех клубов
        """

        foundClubs = _clubService.findAllClubs()
        return render_template('clubs.html', clubs=foundClubs)

    @staticmethod
    @app.route('/club_account/<int:id>', methods=['GET'])
    def get_club_page(id):

        """
        Возвращает страницу клуба
        
        Параметры
        ---------
        id : int
            Идентификатор клуба
        
        Возвращает
        ---------
        club : dict
            Клуб
        head : dict
            Руководитель клуба
        users : list
            Список всех пользователей
        """

        club = _clubService.findClubById(id)
        user_head = _userService.findUser(club.head)
        users = _userService.findAllUsers()
        redact = False
        user = None
        user_clubs = None
        news = [news for news in _newsService.findAllNews() if news.id_club == club.id]
        news = news[::-1]
        events = _eventService.findAllEvents()

        if session.get('user_status') == 0:
            redact = True
        if session.get('user_id'):
            user = _userService.findUser(session.get('user_id'))
            user_clubs = session.get('user_clubs')
            if session.get('user_id') == club.head:
                redact = True

        return render_template('club_account.html', events = events, news = news, club = club, head = user_head, users = users, redact = redact, user = user, user_clubs = user_clubs)

    @staticmethod
    @app.route('/application/<int:club_id>/<int:user_id>', methods=['GET'])
    def get_applicationForm_page(club_id, user_id):

        """
        Возвращает страницу формы заявки
        
        Возвращает
        ---------
        entry_application : html
            Страница формы заявки
        """
        
        return render_template('entry_application.html', club_id = club_id, user_id = user_id)

    @staticmethod
    @app.route('/create_club.html', methods = ['GET'])
    def create_club_page():
        """
        Возвращает страницу добавления клуба

        Возвращает
        ---------
        create_club : html
            Страница добавления клуба
        """

        return render_template('create_club.html')

    @staticmethod
    @app.route('/add_news.html/<int:id>', methods = ['GET'])
    def get_add_news_page(id):
        """
        Возвращает страницу добавления клуба

        Возвращает
        ---------
        create_club : html
            Страница добавления клуба
        """
        path_to_img = None
        date_creation = datetime.date.today()
        club_id = id
        return render_template('add_news.html', club_id = club_id, path_to_img = path_to_img,  date_creation = date_creation)

    @staticmethod
    @app.route('/edit_club/<int:id>', methods=['GET'])
    def get_editClub_page(id):

        """
        Возвращает страницу редактирования клуба

        Возвращает
        ---------
        edit_clubn: html
            Страница редактирования клуба
        """
        club = _clubService.findClubById(id)
        users = _userService.findAllUsers()

        return render_template('edit_club.html', club = club, users = users)

    @staticmethod
    @app.route('/application_club/<int:id>', methods=['GET'])
    def get_applicationsClub_page(id):

        """
        Возвращает страницу редактирования клуба

        Возвращает
        ---------
        edit_clubn: html
            Страница редактирования клуба
        """
        applications = _applicationService.findAllApplications()
        club = _clubService.findClubById(id)
        users = _userService.findAllUsers()

        return render_template('applications.html', applications = applications, club = club, users = users)

    @staticmethod
    @app.route('/admin_panel', methods=['GET'])
    def get_adminPanel_page():

        """
        Возвращает страницу админа

        Возвращает
        ---------
        edit_clubn: html
            Страница редактирования клуба
        """
        applications = _clubApplicationService.findAllClubApplications()
        return render_template('admin_panel.html', applications = applications)
