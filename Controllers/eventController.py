from flask import jsonify, request, render_template
from flask_restful import Resource
from Models.event import Event
from Services.eventService import EventService
from application import app

_eventService = EventService()

class EventController(Resource):

    @staticmethod
    @app.route('/events', methods=['GET'])
    def get_all_events():

        events = _eventService.findAllEvents()

        return jsonify({"events": events})

    @staticmethod
    @app.route('/events/<int:id>', methods=['GET'])
    def get_event(id):

        event = _eventService(id)

        return jsonify(event)

    @staticmethod
    @app.route('/add_event', methods=['POST'])
    def add_event():
        if request.is_json:
            request_data = request.get_json()
            news = Event(
                id_club=request_data["id_club"],
                date_event=request_data["date_event"],
                title_event=request_data["title_event"]
            )

        else:
            id_club = int(request.form.get("id_club")),
            date_event = request.form.get("date_event"),
            title_event= request.form.get("title_event")
            time_event = request.form.get("time")

            event = Event(
                id_club=id_club,
                date_event=date_event,
                title_event=title_event,
                time=time_event
            )

        result = _eventService.addEvent(event)

        return jsonify(result)

    @staticmethod
    @app.route('/delete_event/<int:event_id>', methods=['DELETE'])
    def delete_event(event_id):

        result = _eventService.deleteEvent(event_id)

        return jsonify(result)

