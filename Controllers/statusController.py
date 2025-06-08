from flask import jsonify
from flask_restful import Resource
from Services.statusService import StatusService
from application import app

_statusService = StatusService()

class StatusController(Resource):

    """
    Класс контроллера статусов
    
    ...
    
    Атрибуты
    -------
    _statusService : StatusService
        Сервис статусов
        
    Методы
    -------
    get_stats()
        Возвращает список статусов
    get_status(id)
        Возвращает статус по id
    """

    @staticmethod
    @app.route('/status', methods=['GET'])
    def get_stats():

        """
        Возвращает список статусов

        Возвращает
        ---------
        jsonify({"status": _statusService.findAllStats()})
            Список статусов
        """

        return jsonify({"status": _statusService.findAllStats()})

    @staticmethod
    @app.route('/status/<int:id>', methods=['GET'])
    def get_status(id):

        """
        Возвращает статус по id

        Параметры
        ---------
        id : int
            Идентификатор статуса

        Возвращает
        ---------
        jsonify(status)
            Статус
        """
        
        status = _statusService.findStatus(id)
        return jsonify(status)

