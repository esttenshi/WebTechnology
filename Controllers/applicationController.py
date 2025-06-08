from flask import jsonify, request, redirect, url_for, session
from flask_restful import Resource
from Models.application import Application
from Services.applicationService import ApplicationService
from application import app
from Services.userService import UserService

_applicationService = ApplicationService()
_userService = UserService()

class ApplicationController(Resource):

    """
    Класс контроллера для работы с заявкамм
    
    ...

    Методы
    ------

    get_applications()
        Возвращает все заявки
    get_application(id)
        Возвращает заявку по идентификатору
    delete_application()
        Удаляет аккаунт по идентификатору
    update_application(id)
        Обновляет информацию о заявке по идентификатору
    add_application()
        Добавляет заявку
    """

    @staticmethod
    @app.route('/applications', methods=['GET'])
    def get_applications():

        """
        Возвращает список заявок

        Возвращает
        ---------
        jsonify({{"applications": _applicationService.findAllApplications()})
            Список заявок
        """

        return jsonify({"applications": _applicationService.findAllApplications()})

    @staticmethod
    @app.route('/application/<int:id>', methods=['GET'])
    def get_application(id):

        """
        Возвращает заявку по идентификатору

        Параметры
        ---------
        id : int
            Идентификатор заявки

        Возвращает
        ---------
        jsonify(application)
            Заявка
        """

        application = _applicationService.findApplication(id)
        return jsonify(application)

    @staticmethod
    @app.route('/applications/<int:id>', methods=['DELETE'])
    def delete_application(id):

        """
        Удаляет аккаунт по идентификатору

        Параметры
        ---------
        id : int
            Идентификатор заявки

        Возвращает
        ---------
        jsonify(id)
            Идентификатор заявки
        """

        _applicationService.deleteApplication(id)
        return jsonify(id)

    @staticmethod
    @app.route('/applications', methods=['POST'])
    def add_application():

        """
        Обновляет заявку по идентификатору

        Параметры
        ---------
        id : int
            Идентификатор заявки

        Возвращает
        ---------
        jsonify({"applications": _applicationService.findAllApplications()})
            Список заявок
        """

        if request.is_json:
            request_data = request.get_json()
            application = Application(
                user_id=request_data["user_id"],
                club_id=request_data["club_id"],
                reason=request_data["reason"],
                group_name=request_data["group"])
        else:
            user_id = request.form.get('user_id')
            club_id = request.form.get('club_id')
            reason = request.form.get('reason')
            group_name = request.form.get('group_name')
            application = Application(
                user_id=user_id,
                club_id=club_id,
                reason=reason,
                group_name=group_name)

        _applicationService.addApplication(application)
        return jsonify({"applications": _applicationService.findAllApplications()})

    @staticmethod
    @app.route('/applications/<int:id>', methods=['PUT'])
    def update_application(id):

        """
        Обновляет заявку по идентификатору

        Параметры
        ---------
        id : int
            Идентификатор заявки

        Возвращает  
        ---------
        jsonify({"applications": _applicationService.findAllApplications()})
            Список заявок
        """

        request_data = request.get_json()
        application = Application(
            user_id=request_data["user_id"],
            club_id=request_data["club_user"],
            reason=request_data["reason"],
            group_name=request_data["group_name"])
        _applicationService.updateApplication(id, application)
        return jsonify({"applications": _applicationService.findAllApplications()})

    @staticmethod
    @app.route('/accept_application/<int:application_id>', methods=['PUT'])
    def accept_application(application_id):

        """
        Обновляет заявку по идентификатору

        Параметры
        ---------
        id : int
            Идентификатор заявки

        Возвращает
        ---------
        jsonify({"message": "Application accepted"})
            Сообщение об успешном принятии заявки
        """

        application = _applicationService.findApplication(application_id)
        user = _userService.findUser(application.user_id)
        _userService.updateUserClubs(user.id, user, application.club_id)
        _applicationService.deleteApplication(application_id)
        return jsonify({"message": "Заявка на вступление принята"})

    @staticmethod
    @app.route('/reject_application/<int:application_id>', methods=['DELETE'])
    def reject_application(application_id):

        """
        Обновляет заявку по идентификатору

        Параметры
        ---------
        id : int
            Идентификатор заявки

        Возвращает
        ---------
        jsonify({"applications": _applicationService.findAllApplications()})
            Список заявок
        """
        _applicationService.deleteApplication(application_id)
        return jsonify({"applications": _applicationService.findAllApplications()})

