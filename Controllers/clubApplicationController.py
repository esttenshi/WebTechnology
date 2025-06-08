from flask import jsonify, request, session
from flask_restful import Resource

from Controllers.accountController import isLogged
from Models.clubApplication import ClubApplication
from Services.clubApplicationService import ClubApplicationService
from Services.clubService import ClubService
from application import app
from Models.club import Club
_clubApplicationService = ClubApplicationService()
_clubService = ClubService()

class ClubApplicationController(Resource):

    @staticmethod
    @app.route('/club_applications', methods=['GET'])
    def get_club_applications():

        return jsonify({"club_applications": _clubApplicationService.findAllClubApplications()})

    @staticmethod
    @app.route('/club_applications/<int:id>', methods=['GET'])
    def get_club_application(id):

        club_application = _clubApplicationService.findClubApplication(id)
        return jsonify(club_application)

    @staticmethod
    @app.route('/club_applications', methods=['POST'])
    def add_club_application():
        if request.is_json:
            request_data = request.get_json()
            club_application = ClubApplication(
                title=request_data["title"],
                head=session['user_id'],  # Предполагается, что user_id хранится в сессии
                description=request_data["description"]
            )
        else:
            title = request.form.get("title")
            description = request.form.get("description")
            path_to_img=request.form.get("path_to_img")

            club_application = ClubApplication(
                title=title,
                head=session['user_id'],  # Предполагается, что user_id хранится в сессии
                description=description,
                path_to_img=path_to_img
            )
        _clubApplicationService.addClubApplication(club_application)
        return jsonify({"message": "Заявка на создание клуба успешно добавлена."})

    @staticmethod
    @app.route('/club_applications/<int:id>', methods=['PUT'])
    def update_club_application(id):

        request_data = request.get_json()
        club_application = ClubApplication(
            title=request_data["title"],
            head=session['user_id'],
            description=request_data["description"],
        path_to_img=request_data)
        _clubApplicationService.updateClubApplication(id, club_application)
        return jsonify({"club_applications": _clubApplicationService.findAllClubApplications()})

    @staticmethod
    @app.route('/club_applications/<int:id>', methods=['DELETE'])
    def delete_club_application(id):

        return jsonify({"message": _clubApplicationService.deleteClubApplication(id)})

    @staticmethod
    @app.route('/accept_club_application/<int:club_application_id>', methods=['POST'])
    def accept_club_application(club_application_id):

        club_application = _clubApplicationService.findClubApplication(club_application_id)

        if not club_application:
            return jsonify({'Сообщение': 'Заявка не найдена'}), 404

        # Продолжаем обработку заявки

        club = Club(title=club_application.title,
                    head = club_application.head,
                    connection=club_application.head,
                    description=club_application.description,
                    path_to_img=club_application.path_to_img)

        _clubService.addClub(club, session.get('user_status'))  # Передаем объект club_application

        _clubApplicationService.deleteClubApplication(club_application_id)

        return jsonify({"message": "Заявка на вступление принята"})

    @staticmethod
    @app.route('/reject_club_application/<int:application_id>', methods=['DELETE'])
    def reject_club_application(club_application_id):

        _clubApplicationService.deleteClubApplication(club_application_id)
        return jsonify({"applications": _clubApplicationService.findAllClubApplications()})

