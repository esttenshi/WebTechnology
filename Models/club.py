from dataclasses import dataclass

@dataclass
class Club:

    """
    Класс клуба

    ...

    Атрибуты
    -------
    id : int
        Идентификатор клуба
    title : str
        Название клуба
    head : int
        Идентификатор руководителя клуба
    connection : int
        Идентификатор участника клуба
    """
    
    id: int = None
    title: str = None
    head: int = None
    connection: int = None
    description: str = None
    path_to_img: str = None

    