from flask import jsonify, request, session
from flask_restful import Resource
from Models.user import User
from Services.userService import UserService
from application import app

_userService = UserService()

class UserController(Resource):

    """
    Класс контроллера для работы с пользователями
    
    ...
    
    Атрибуты
    -------
    _userService : UserService
        Сервис для работы с пользователями
    
    Методы
    ------
    get_users()
        Возвращает список всех пользователей
    get_user(id)
        Возвращает пользователя по идентификатору
    delete_user(id)
        Удаляет пользователя по идентификатору
    update_user(id)
        Обновляет пользователя по идентификатору
    """

    @staticmethod
    @app.route('/users', methods=['GET'])
    def get_users():

        """
        Возвращает список всех пользователей

        Возвращает
        ---------
        users : list
            Список всех пользователей
        """

        return jsonify({"users": _userService.findAllUsers()})

    @staticmethod
    @app.route('/users/<int:id>', methods=['GET'])
    def get_user(id):

        """
        Возвращает пользователя по идентификатору

        Параметры
        ---------
        id : int
            Идентификатор пользователя

        Возвращает
        ---------
        user : dict
            Пользователь
        """

        user = _userService.findUser(id)
        return jsonify(user)

    @staticmethod
    @app.route('/users/<int:id>', methods=['DELETE'])
    def delete_user(id):

        """
        Удаляет пользователя по идентификатору

        Параметры
        ---------
        id : int
            Идентификатор пользователя

        Возвращает
        ---------
        id : int
            Идентификатор пользователя
        """

        _userService.deleteUser(id)
        return jsonify(id)

    @staticmethod
    @app.route('/users/<int:id>', methods=['PUT'])
    def update_user(id):

        """
        Обновляет пользователя по идентификатору

        Параметры
        ---------
        id : int
            Идентификатор пользователя
        surname : str
            Фамилия пользователя
        name : str
            Имя пользователя
        patronymic : str
            Отчество пользователя
        status : int
            Статус пользователя

        Возвращает
        ---------
        users : list
            Список всех пользователей
        """

        request_data = request.get_json()
        user = User(
            surname=request_data["surname"],
            name=request_data["name"],
            patronymic=request_data["patronymic"],
            status=_userService.findUser(id).status)

        _userService.updateUser(id, user)
        return jsonify({"users": _userService.findAllUsers()})

    @staticmethod
    @app.route('/users/<int:club_id>/<int:user_id>', methods=['DELETE'])
    def exit_club(club_id, user_id):

        """
        Удаляет клуб из списка клубов пользователя

        Параметры
        ---------
        club_id : int
            Идентификатор клуба
        user_id : int
            Идентификатор пользователя

        Возвращает
        ---------
        user.clubs : list
            Список клубов пользователя
        """

        user = _userService.findUser(user_id)
        user_clubs = _userService.deleteClub(club_id, user_id, user.clubs)
        session['user_clubs'] = user_clubs

        return jsonify(user_clubs)