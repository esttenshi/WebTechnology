from flask import jsonify, request, render_template, session
from flask_restful import Resource
from werkzeug.utils import secure_filename

from Models.club import Club
from Services.clubService import ClubService
from Services.userService import UserService
from application import app

_clubService = ClubService()
_userService = UserService()


def allowed_file(filename):
    pass


class ClubController(Resource):

    """
    Класс контроллера для работы с клубами
    
    ...
    
    Атрибуты
    -------
    _clubService : ClubService
        Сервис для работы с клубами
    _userService: UserService
        Сервис для работы с пользователями
        
    Методы
    ------
    get_clubs()
        Возвращает список всех клубов
    get_club(title)
        Возвращает клуб по названию
    add_club()
        Добавляет новый клуб
    update_club(id)
        Обновляет клуб
    delete_club(id)
        Удаляет клуб
    """

    @staticmethod
    @app.route('/clubs', methods=['GET'])
    def get_clubs():

        """
        Возвращает список всех клубов
    
        Возвращает  
        ---------
        clubs : list
            Список всех клубов
        """
        clubs = _clubService.findAllClubs()
        return render_template('clubs.html', clubs=clubs)

    @staticmethod
    @app.route('/clubs/<title>', methods=['GET'])
    def get_club(title):

        """
        Возвращает клуб по названию
    
        Параметры
        ---------
        title : str
            Название клуба
    
        Возвращает
        ---------
        club : dict
            Клуб
        """

        club = _clubService.findClub(title)
        return jsonify(club)

    @staticmethod
    @app.route('/clubs', methods=['POST'])
    def add_club():
        """
        Добавляет новый клуб

        Параметры
        ---------
        title : str
            Название клуба
        head : int
            Идентификатор пользователя, создавшего клуб
        connection : int
            Идентификатор пользователя, подключенного к клубу
        description : str
            Описание клуба
        path_to_img : str
            Путь к изображению клуба

        Возвращает
        ---------
        club : dict
            Клуб
        """
        if request.is_json:
            request_data = request.get_json()
            club = Club(
                title=request_data["title"],
                head=request_data["head"],
                connection=request_data["connection"],
                description=request_data["description"],
                path_to_img=request_data["path_to_img"]
            )
        else:
            title = request.form.get("title")
            head = int(request.form.get("head"))
            connection = int(request.form.get("connection"))
            description = request.form.get("description")
            photo = request.files['photo']  # Получаем файл изображения

            # Сохраняем изображение в папку ../static/images/clubs с именем клуба
            if photo and allowed_file(photo.filename):
                filename = secure_filename(photo.filename)
                path_to_img = f'.../static/images/clubs/{title[0]}.jpg'
                photo.save(path_to_img)

            club = Club(
                title=title,
                head=head,
                connection=connection,
                description=description,
                path_to_img=path_to_img
            )

        result = _clubService.addClub(club)
        return jsonify(result)

    @staticmethod
    @app.route('/clubs/<int:id>', methods=['PUT'])
    def update_club(id):

        """
        Обновляет клуб
        
        Параметры
        ---------
        id : int
            Идентификатор клуба
        title : str
            Название клуба
        head : int
            Идентификатор руководителя клуба
        connection : int
            Идентификатор участника клуба
            
        Возвращает
        ---------
        club : dict
            Клуб
        """

        request_data = request.get_json()
        club = Club(
            title=request_data["title"],
            head=request_data["head"],
            connection=request_data["connection"],
            description=request_data["description"],
            path_to_img=request_data["path_to_img"])

        user_id = session.get('user_id')  # Получаем id пользователя из сессии или иным способом

        # Проверяем права пользователя на обновление клуба
        user_status = _userService.findUser(user_id).status
        result = _clubService.updateClub(id, club, user_status)
        return jsonify(result)

    @staticmethod
    @app.route('/clubs/<int:id>', methods=['DELETE'])
    def delete_club(id):

        """
        Удаляет клуб
    
        Параметры
        ---------
        id : int
            Идентификатор клуба
    
        Возвращает
        ---------
        club : dict
            Клуб
        """
        
        # прописываем в теле "user_id": "1"
        request_data = request.get_json()
        user_status = _userService.findUser(request_data["user_id"]).status
        result = _clubService.deleteClub(id, user_status)
        return jsonify(result)

