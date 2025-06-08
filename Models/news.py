from dataclasses import dataclass
from datetime import date

@dataclass
class News:

    """
    Класс новости

    ...

    Атрибуты
    -------
    id : int
        Идентификатор новости
    id_club : int
        Идентификатор клуба
    date_creation : date
        Дата создания новости
    title : str
        Название новости
    news_text : str
        Текст новости
    path_to_img : str
        Путь к изображению новости
    """
    id: int = None
    id_club: int = None
    date_creation: date = None
    title: str = None
    news_text: str = None
    path_to_img: str = None


