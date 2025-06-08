from dataclasses import dataclass

@dataclass
class User:

    """
    Класс пользователя

    ...

    Атрибуты
    -------
    id : int
        Идентификатор пользователя
    surname : str
        Фамилия пользователя
    name : str
        Имя пользователя
    patronymic : str
        Отчество пользователя
    status : str
        Статус пользователя
    clubs : int
        Количество клубов пользователя
    """
    
    id: int = None
    surname: str = None
    name: str = None
    patronymic: str = None
    status: str = None
    clubs: int = None

