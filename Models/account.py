from dataclasses import dataclass

@dataclass
class Account:

    """
    Класс аккаунта

    ...

    Атрибуты
    -------
    id : int
        Идентификатор аккаунта
    login : str
        Логин аккаунта
    password : str
        Пароль аккаунта

    Методы
    ------
    serialize
        Возвращает аккаунт в виде словаря
    """
    id: int = None
    login: str = None
    password: str = None

    def serialize(self):

        """
        Возвращает аккаунт в виде словаря
        
        Возвращает
        -------
        {"id": self.id,
        "login": self.login,
        "pass": self.password
        } 
        """

        return {"id": self.id,
                "login": self.login,
                "pass": self.password,
                "fileSize": self.fileSize,
                "fileDateCreation": self.fileDateCreation,
                "fileChange": self.fileChange,
                "fileType": self.fileType
                }