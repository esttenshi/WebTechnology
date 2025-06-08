from application import con
from Models.user import User

class UserService:

    """
    Класс для работы с пользователями

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
    status : int
        Статус пользователя
    clubs : str
        Клубы, в которых находится пользователь

    Методы
    ------
    def findUser(self, id)
        Поиск пользователя по идентификатору
    def findAllUsers(self)
        Поиск всех пользователей
    def deleteUser(self, id)
        Удаление пользователя
    def updateUser(self, id, user_object: User)
        Обновление пользователя
    """

    def findUser(self, id):

        """
        Поиск пользователя по идентификатору

        Параметры
        ---------
        id : int
            Идентификатор пользователя

        Возвращает
        ---------
        user : dict
            Пользователь
        """

        with con:
            sql_select = """SELECT 
                               id,
                               surname,
                               name,
                               patronymic,
                               status,
                               clubs
                            FROM 
                                users
                            WHERE 
                                id = ?"""
            raw_user = con.execute(sql_select, (id,)).fetchone()
            user = User(
                id=raw_user[0],
                surname=raw_user[1],
                name=raw_user[2],
                patronymic=raw_user[3],
                status=raw_user[4],
                clubs=raw_user[5],
            )
        return user

    def findAllUsers(self):

        """
        Поиск всех пользователей

        Возвращает
        ---------
        users : list
            Список всех пользователей
        """

        users = []
        with con:
            sql_select = """SELECT 
                               id,
                               surname,
                               name,
                               patronymic,
                               status,
                               clubs
                            FROM users"""
            raw_users = con.execute(sql_select).fetchall()
            for row in raw_users:
                user = User(
                    id=row[0],
                    surname=row[1],
                    name=row[2],
                    patronymic=row[3],
                    status=row[4],
                    clubs=row[5])
                users.append(user)
        return users

    def deleteUser(self, id):

        """
        Удаление пользователя

        Параметры
        ---------
        id : int
            Идентификатор пользователя

        Возвращает
        ---------
        id : int
            Идентификатор пользователя
        """

        with con:
            sql_delete_accounts = """DELETE FROM accounts WHERE id = ?"""
            con.execute(sql_delete_accounts, (id,))

            sql_delete_users = """DELETE FROM users WHERE id = ?"""
            con.execute(sql_delete_users, (id,))


    def updateUser(self, id, user_object: User):

        """
        Обновление пользователя

        Параметры
        ---------
        id : int
            Идентификатор пользователя
        user_object : User
            Объект пользователя

        Возвращает
        ---------
        None
        """
        
        with con:
            sql_update = """UPDATE 
                              users
                            SET
                              surname = ?,
                              name = ?,
                              patronymic = ?,
                              status = ?
                            WHERE
                              id = ?"""
            con.execute(sql_update, (user_object.surname,
                                     user_object.name,
                                     user_object.patronymic,
                                     user_object.status,
                                     id))

    def updateUserClubs(self, id, user_object: User, club_id):

        """
        Обновление пользователя

        Параметры
        ---------
        id : int
            Идентификатор пользователя
        user_object : User
            Объект пользователя

        Возвращает
        ---------
        None
        """
        clubs = user_object.clubs if user_object.clubs else ""  # Инициализация переменной clubs, если она пуста
        clubs += f' {club_id}'

        with con:
            sql_update = """UPDATE 
                                  users
                                SET
                                  clubs = ?
                                WHERE
                                  id = ?"""
            con.execute(sql_update, (clubs, id))

    def deleteClub(self, club_id, user_id, user_clubs):

        """
        Удаляет клуб из списка клубов пользователя

        Параметры
        ---------
        club_id : int
            Идентификатор клуба
        user_id : int
            Идентификатор пользователя

        Возвращает
        ---------
        user.clubs : list
            Список клубов пользователя
        """
        user_clubs = user_clubs.split(' ')
        user_clubs.remove(str(club_id))
        user_clubs = ' '.join(user_clubs)

        with con:
            sql_update = """UPDATE 
                                  users
                                SET
                                  clubs = ?
                                WHERE
                                  id = ?"""
            con.execute(sql_update, (user_clubs, user_id))

        return user_clubs