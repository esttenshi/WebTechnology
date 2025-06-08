from application import con
from Models.news import News

class NewsService:

    """
    Класс для работы с новостями

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

    Методы
    -------
    findNews(title)
        Возвращает новость по названию
    findAllNews()
        Возвращает список всех новостей
    addNews(news_object, user_status)
        Добавляет новость
    updateNews(news_object, user_status)
        Обновляет новость
    deleteNews(id, user_status)
        Удаляет новость
    """

    def findNews(self, title):

        """
        Возвращает новость по названию

        Параметры
        ---------
        title : str
            Название новости

        Возвращает
        ---------
        news : dict
            Новость
        """

        with con:
            sql_select = """SELECT 
                               id,
                               id_club,
                               date_creation,
                               title,
                               news_text,
                               path_to_img
                            FROM news
                            WHERE title = ?"""
            raw_news = con.execute(sql_select, (title,)).fetchone()
            news = News(
                id=raw_news[0],
                id_club=raw_news[1],
                date_creation=raw_news[2],
                title=raw_news[3],
                news_text=raw_news[4],
                path_to_img=raw_news[5]
            )
        return news

    def findAllNews(self):

        """
        Возвращает список всех новостей

        Возвращает
        ---------
        news : list
            Список всех новостей
        """

        all_news = []
        with con:
            sql_select = """SELECT 
                               id,
                               id_club,
                               date_creation,
                               title,
                               news_text,
                               path_to_img
                            FROM news"""
            raw_news = con.execute(sql_select).fetchall()

            for row in raw_news:
                news = News(
                    id=row[0],
                    id_club=row[1],
                    date_creation=row[2],
                    title=row[3],
                    news_text=row[4],
                    path_to_img=row[5])
                all_news.append(news)

        return all_news

    def addNews(self, news_object: News):

        """
        Добавляет новость

        Параметры
        ---------
        news_object : News
            Новость
        user_status : int
            Статус пользователя

        Возвращает
        ---------
        news : dict
            Новость
        """

        with con:
            sql_insert = """INSERT INTO news
                            (id_club, date_creation, title, news_text, path_to_img) 
                            values(?, ?, ?, ?, ?)"""
            con.execute(sql_insert, (news_object.id_club[0],
                                     news_object.date_creation[0],
                                     news_object.title[0],
                                     news_object.news_text[0],
                                     news_object.path_to_img))
            return {"message": "Новость успешно добавлена."}

    def updateNews(self, id, news_object: News, user_status):

        """
        Обновляет новость

        Параметры
        ---------
        id : int
            Идентификатор новости
        news_object : News
            Новость
        user_status : int
            Статус пользователя

        Возвращает
        ---------
        news : dict
            Новость
        """

        if user_status in [1, 2]:
            with con:
                sql_update = """UPDATE news
                                SET
                                  id_club = ?,
                                  date_creation = ?,
                                  title = ?,
                                  news_text = ?,
                                  path_to_img = ?
                                WHERE
                                  id = ?"""
                con.execute(sql_update, (news_object.id_club,
                                         news_object.date_creation,
                                         news_object.title,
                                         news_object.news_text,
                                         news_object.path_to_img,
                                         id))
                return {"message": "Новость успешно обновлена."}
        else:
            return {"error": "У вас нет прав на обновление новости."}

    def deleteNews(self, id, user_status):

        """
        Удаляет новость

        Параметры
        ---------
        id : int
            Идентификатор новости
        user_status : int
            Статус пользователя

        Возвращает
        ---------
        news : dict
            Новость
        """
        
        if user_status in [1, 2]:
            with con:
                sql_delete_news = """DELETE FROM news WHERE id = ?"""
                con.execute(sql_delete_news, (id,))
                return {"message": "Новость успешно удалена."}
        else:
            return {"error": "У вас нет прав на удаление новости."}