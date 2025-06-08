from dataclasses import dataclass

@dataclass
class Application:

    """
    Класс клуба

    ...

    Атрибуты
    -------
    id : int
        Идентификатор клуба
    club_id : int
        Идентификатор клуба, в который подается заявка
    user_id : int
        Идентификатор пользователя, который подает заявку
    reason : str
        Причина вступления
    group : str
        Группа пользователя, который подает заявку
    """

    id: int = None
    club_id: int = None
    user_id: int = None
    reason: str = None
    group_name: str = None

