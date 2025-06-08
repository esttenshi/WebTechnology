from flask import jsonify, request, render_template
from flask_restful import Resource
from Models.news import News
from Services.newsService import NewsService
from Services.clubService import ClubService
from Services.userService import UserService
from application import app
import datetime

_newsService = NewsService()
_clubService = ClubService()
_userService = UserService()

class NewsController(Resource):

    """
    Класс контроллера для работы с новостями
    
    ...
    
    Атрибуты
    -------
    _newsService : NewsService
        Сервис для работы с новостями
    _clubService : ClubService
        Сервис для работы с клубами
    _userService: UserService
        Сервис для работы с пользователями
        
    Методы
    ------
    get_all_news()
        Возвращает список всех новостей
    get_news(title)
        Возвращает новость по названию
    add_news()
        Добавляет новость
    update_news(id)
        Обновляет новость
    delete_news(id)
        Удаляет новость
    """

    @staticmethod
    @app.route('/news', methods=['GET'])
    def get_all_news():

        """
        Возвращает список всех новостей
    
        Возвращает  
        ---------
        news : list
            Список всех новостей
        """

        news = _newsService.findAllNews()
        clubs = _clubService.findAllClubs()
        return render_template('news.html', news=news, clubs=clubs)

    @staticmethod
    @app.route('/news/<title>', methods=['GET'])
    def get_news(title):

        """
        Возвращает новость по названию
    
        Параметры
        ---------
        title : str
            Название новости

        Возвращает
        ---------
        news : dict
            Новость
        """

        news = _newsService.findNews(title)
        return jsonify(news)

    @staticmethod
    @app.route('/add_news', methods=['POST'])
    def add_news():

        """
        Добавляет новость

        Параметры
        ---------
        id_club : int
            Идентификатор клуба
        date_creation : date
            Дата создания новости
        title : str
            Название новости
        news_text : str
            Текст новости
        path_to_img : str
            Путь к изображению новости
            
        Возвращает
        ---------
        news : dict
            Новость
        """
        if request.is_json:
            request_data = request.get_json()
            news = News(
                id_club=request_data["id_club"],
                date_creation=request_data["date_creation"],
                title=request_data["title"],
                news_text=request_data["news_text"],
                path_to_img=request_data["path_to_img"]
            )

        else:
            id_club = int(request.form.get("id_club")),
            date_creation = datetime.date.today(),
            title = request.form.get("title"),
            news_text = request.form.get("news_text"),
            photo = request.files['photo']
            if photo:
                path_to_img = f'../static/images/news/{title[0]}.jpg'
                photo.save(f'Static/images/news/{title[0]}.jpg')

            news = News(
                id_club=id_club,
                date_creation=date_creation,
                title=title,
                news_text=news_text,
                path_to_img=path_to_img
            )

        result = _newsService.addNews(news)

        return jsonify(result)

    @staticmethod
    @app.route('/news/<int:id>', methods=['PUT'])
    def update_news(id):

        """
        Обновляет новость

        Параметры
        ---------
        id : int
            Идентификатор новости
        id_club : int
            Идентификатор клуба
        date_creation : date
            Дата создания новости
        title : str
            Название новости
        news_text : str
            Текст новости
        path_to_img : str
            Путь к изображению новости
            
        Возвращает
        ---------
        news : dict
            Новость
        """


        request_data = request.get_json()
        news = News(
            id_club=request_data["id_club"],
            date_creation=request_data["date_creation"],
            title=request_data["title"],
            news_text=request_data["news_text"],
            path_to_img=request_data["path_to_img"]
        )
        # прописываем в теле "user_id": "1"
        user_status = _userService.findUser(request_data["user_id"]).status
        result = _newsService.updateNews(id, news, user_status)
        return jsonify(result)

    @staticmethod
    @app.route('/news/<int:id>', methods=['DELETE'])
    def delete_news(id):

        """
        Удаляет новость

        Параметры
        ---------
        id : int
            Идентификатор новости

        Возвращает
        ---------
        news : dict
            Новость
        """

        # прописываем в теле "user_id": "1"
        user_status = _userService.findUser(id).status
        result = _newsService.deleteNews(id, user_status)
        return jsonify(result)

    @staticmethod
    def get_club_title(club_id):

        """
        Возвращает название клуба по его идентификатору

        Параметры
        ---------
        club_id : int
            Идентификатор клуба

        Возвращает
        ---------
        title : str
            Название клуба
        """
        
        club = _clubService.findClubById(club_id)
        return club.title if club else "Unknown Club"

    @staticmethod
    @app.route('/load-more-news', methods=['GET'])
    def load_more_news():
        start_index = request.args.get('start', type=int)
        end_index = request.args.get('end', type=int)

        news = _newsService.findAllNews()
        news = news[start_index:end_index]

        clubs = _clubService.findAllClubs()

        for item in news:
            club = next((club for club in clubs if club.id == item.id_club), None)
            if club:
                item.id_club = club.title
            else:
                item.id_club = 'Название клуба не найдено'

        if len(news) == 0:
            return jsonify({"message": "Новостей больше нет"})

        return jsonify({"news": news})