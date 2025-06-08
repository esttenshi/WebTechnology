from application import con
from Models.club import Club

class ClubService:

    """
    Класс для работы с клубами
    
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
    
    Методы
    -------
    findClub(self, title)
        Поиск клуба по названию
    findClubById(self, club_id)
        Посик клуба по идентификатору
    findAllClubs(self)
        Возвращает список всех клубов
    addClub(self, club_object)
        Добавляет новый клуб
    updateClub(self, id, club_object)
        Обновляет клуб
    deleteClub(self, id)
        Удаляет клуб
    """
    def findClub(self, title):

        """
        Поиск клуба по названию

        Параметры
        ---------
        title : str
            Название клуба

        Возвращает
        ---------
        club : dict
            Клуб
        """

        with con:
            sql_select = """SELECT 
                               id,
                               title,
                               head,
                               connection,
                               description,
                               path_to_img
                            FROM clubs
                            WHERE title = ?"""
            raw_clubs = con.execute(sql_select, (title,)).fetchone()
            club = Club(
                id=raw_clubs[0],
                title=raw_clubs[1],
                head=raw_clubs[2],
                connection=raw_clubs[3],
                description=raw_clubs[4],
                path_to_img=raw_clubs[5]
            )
        return club

    def findClubById(self, club_id):

        """
        Поиск клуба по идентификатору

        Параметры
        ---------
        club_id : int
            Идентификатор клуба

        Возвращает
        ---------
        club : dict
            Клуб
        """

        with con:
            sql_select = """SELECT 
                               id,
                               title,
                               head,
                               connection,
                               description,                              
                               path_to_img
                            FROM clubs
                            WHERE id = ?"""
            raw_club = con.execute(sql_select, (club_id,)).fetchone()
            if raw_club:
                club = Club(
                    id=raw_club[0],
                    title=raw_club[1],
                    head=raw_club[2],
                    connection=raw_club[3],
                    description=raw_club[4],
                    path_to_img=raw_club[5]
                )
                return club

    def findAllClubs(self):

        """
        Возвращает список всех клубов

        Возвращает
        ---------
        clubs : list
            Список всех клубов
        """

        clubs = []
        with con:
            sql_select = """SELECT 
                               id,
                               title,
                               head,
                               connection,
                               description,                               
                               path_to_img
                            FROM clubs"""
            raw_clubs = con.execute(sql_select).fetchall()

            for row in raw_clubs:
                club = Club(
                    id=row[0],
                    title=row[1],
                    head=row[2],
                    connection=row[3],
                    description=raw_clubs[4],
                    path_to_img=raw_clubs[5])
                clubs.append(club)
        return clubs

    def addClub(self, club_object: Club, user_status):

        """
        Добавляет новый клуб

        Параметры
        ---------
        title : str
            Название клуба
        head : int
            Идентификатор пользователя, создавшего клуб
        connection : int
            Идентификатор пользователя, подключенного к клубу
            
        Возвращает
        ---------
        club : dict
            Клуб
        """

        with con:
            sql_insert = """INSERT INTO clubs
                            (title, head, connection, description, path_to_img) 
                            values(?, ?, ?, ?, ?)"""
            con.execute(sql_insert, (club_object.title,
                                     club_object.head,
                                     club_object.connection,
                                     club_object.description,
                                     club_object.path_to_img))
            return {"message": "Клуб успешно добавлен."}

    def updateClub(self, id, club_object: Club, user_status):

        """
        Обновляет клуб

        Параметры
        ---------
        id : int
            Идентификатор клуба
        title : str
            Название клуба
        head : int
            Идентификатор пользователя, создавшего клуб
            
        Возвращает
        ---------
        club : dict
            Клуб
        """


        with con:
            sql_update = """UPDATE clubs
                            SET
                              title = ?,
                              head = ?,
                              connection = ?,
                              description = ?,                           
                              path_to_img = ?  
                            WHERE
                              id = ?"""
            con.execute(sql_update, (club_object.title,
                                     club_object.head,
                                     club_object.connection,
                                     club_object.description,
                                     club_object.path_to_img,
                                     id))
            return {"message": "Клуб успешно обновлен."}

    def deleteClub(self, id, user_status):

        """
        Удаляет клуб

        Параметры
        ---------
        id : int
            Идентификатор клуба
            
        Возвращает
        ---------
        club : dict
            Клуб
        """

        with con:
            sql_delete_club = """DELETE FROM clubs WHERE id = ?"""
            con.execute(sql_delete_club, (id,))
            return {"message": "Клуб успешно удален."}

