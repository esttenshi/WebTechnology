from dataclasses import dataclass

@dataclass
class Event:

    id: int = None
    id_club: int = None
    date_event: str = None
    title_event: str = None
    time: str = None

    def serialize(self):

        return {"id": self.id,
                "id_club": self.id_club,
                "date_event": self.date_event,
                "title_event": self.title_event,
                "time": self.time
                }