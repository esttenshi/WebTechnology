from dataclasses import dataclass

@dataclass
class Status: 

    """
    Класс статуса

    ...

    Атрибуты
    -------
    id : int
        Идентификатор статуса
    title : str
        Название статуса
    """
    
    id: int = None
    title: str = None