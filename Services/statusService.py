from application import con
from Models.status import Status

class StatusService:

    """
    Сервис статусов

    ...

    Атрибуты
    -------
    id : int
        Идентификатор статуса
    title : str
        Название статуса

    Методы
    -------
    findStatus(id)
        Возвращает статус по id
    findAllStats()
        Возвращает список всех статусов
    """

    def findStatus(self, id):

        """
        Возвращает статус по id

        Параметры
        ---------
        id : int
            Идентификатор статуса

        Возвращает
        ---------
        status : Status
            Статус
        """

        with con:
            sql_select = """SELECT 
                               id,
                               title
                            FROM status
                            WHERE id = ?"""
            raw_stats = con.execute(sql_select, (id,)).fetchone()
            status = Status(
                id=raw_stats[0],
                title=raw_stats[1]
            )
        return status

    def findAllStats(self):

        """
        Возвращает список всех статусов

        Возвращает
        ---------
        status : list
            Список статусов
        """

        status = []
        with con:
            sql_select = """SELECT 
                               id,
                               title
                            FROM status"""
            raw_stats = con.execute(sql_select).fetchall()
            for row in raw_stats:
                stat = Status(
                    id=row[0],
                    title=row[1])
                status.append(stat)
        return status
