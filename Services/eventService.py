from application import con
from Models.event import Event

class EventService:

    def findEvent(self, id):

        with con:
            sql_select = """SELECT 
                               id,
                               id_club,
                               date_event,
                               title_event,
                               time
                            FROM events
                            WHERE id = ?"""

            raw_event = con.execute(sql_select, (id,)).fetchone()

            event = Event(
                id=raw_event[0],
                id_club=raw_event[1],
                date_event=raw_event[2],
                title_event=raw_event[3],
                time=raw_event[4]
            )

        return event

    def findAllEvents(self):


        all_events = []

        with con:
            sql_select = """SELECT 
                              id,
                               id_club,
                               date_event,
                               title_event, 
                               time
                            FROM events"""

            raw_events = con.execute(sql_select).fetchall()

            for raw in raw_events:

                event = Event(
                    id=raw[0],
                    id_club=raw[1],
                    date_event=raw[2],
                    title_event=raw[3],
                    time=raw[4]
                )

                all_events.append(event)

        return all_events

    def addEvent(self, event_object: Event):

        print(event_object.id_club,
              event_object.date_event,
              event_object.title_event,
              event_object.time)
        with con:
            sql_insert = """INSERT INTO events
                            (id_club, date_event, title_event, time) 
                            values(?, ?, ?, ?)"""

            con.execute(sql_insert, (event_object.id_club[0],
                                     event_object.date_event[0],
                                     event_object.title_event,
                                     event_object.time))

            return {"message": "Событие добавлено"}

    def deleteEvent(self, id, user_status):

        if user_status in [1, 2]:
            with con:
                sql_delete_news = """DELETE FROM events WHERE id = ?"""
                con.execute(sql_delete_news, (id,))
                return {"message": "Событие успешно удалено"}
        else:
            return {"error": "У вас нет прав на события"}