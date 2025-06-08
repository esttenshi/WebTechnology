from application import con
from Models.application import Application

class ApplicationService:

    """
    Класс для работы с заявками

    ...

    Атрибуты
    -------
    id : int
        Идентификатор заявки
    club_id : int
        Идентификатор клуба, в который подается заявка
    user_id : str
        Идентификатор пользователя, который отправляет заявку
    reason : str
        Причина заявки
    group : int
        Группа, в которой учится пользователь

    Методы
    ------
    def findApplication(self, id)
        Поиск заявки по идентификатору
    def findAllApplication(self)
        Поиск всех заявок
    def deleteApplication(self, id)
        Удаление заявки
    def addApplication(self, application_object: Application)
        Добавление заявки
    def updateApplication(self, id, application_object: Application)
        Обновление заявки
    """

    def findApplication(self, id):

        """
        Поиск заявки по идентификатору

        Параметры
        ---------
        id : int
            Идентификатор заявки

        Возвращает
        ---------
        application : dict
            Заявка
        """

        with con:
            sql_select = """SELECT 
                               id,
                               club_id,
                               user_id,
                               reason,
                               group_name
                            FROM 
                                applications
                            WHERE 
                                id = ?"""
            raw_application = con.execute(sql_select, (id,)).fetchone()
            application = Application(
                id=raw_application[0],
                club_id=raw_application[1],
                user_id=raw_application[2],
                reason=raw_application[3],
                group_name=raw_application[4]
            )
        return application

    def findAllApplications(self):

        """
        Поиск всех заявок

        Возвращает
        ---------
        applications : dict
            Список всех заявок
        """

        applications = []
        with con:
            sql_select = """SELECT 
                               id,
                               club_id,
                               user_id,
                               reason,
                               group_name
                            FROM applications"""
            raw_applications = con.execute(sql_select).fetchall()
            for row in raw_applications:
                application = Application(
                    id=row[0],
                    club_id=row[1],
                    user_id=row[2],
                    reason=row[3],
                    group_name=row[4])
                applications.append(application)
        return applications

    def deleteApplication(self, id):

        """
        Удаление заявки

        Параметры
        ---------
        id : int
            Идентификатор заявки

        Возвращает
        ---------
        id : int
            Идентификатор заявки
        """

        with con:
            sql_delete_application = """DELETE FROM applications WHERE id = ?"""
            con.execute(sql_delete_application, (id,))

    def addApplication(self, application_object: Application):

        """
        Добавляет заявку

        Параметры
        ---------
        application_object : Application
            Заявка


        Возвращает
        ---------
        {"message": "Заявка отправлена."}
            Сообщение об удачной отправке заявки
        """

        with con:
            sql_insert = """INSERT INTO applications
                            (club_id, user_id, reason, group_name) 
                            values(?, ?, ?, ?)"""
            con.execute(sql_insert, (application_object.club_id,
                                     application_object.user_id,
                                     application_object.reason,
                                     application_object.group_name))
            return {"message": "Заявка отправлена."}

    def updateApplication(self, id, application_object: Application):

        """
        Обновление заявки

        Параметры
        ---------
        id : int
            Идентификатор заявки
        application_object: Application
            Объект заявки

        Возвращает
        ---------
        None
        """

        with con:
            sql_update = """UPDATE 
                              users
                            SET
                              club_id = ?,
                              user_id = ?,
                              reason = ?,
                              group_name = ?
                            WHERE
                              id = ?"""

            con.execute(sql_update, (application_object.club_id,
                                     application_object.user_id,
                                     application_object.reason,
                                     application_object.group_name,
                                     id))