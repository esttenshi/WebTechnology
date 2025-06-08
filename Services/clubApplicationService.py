from application import con
from Models.clubApplication import ClubApplication

class ClubApplicationService:

    def findClubApplication(self, id):

        with con:
            sql_select = """SELECT id, title, head, description 
                            FROM club_applications
                            WHERE id = ?"""
            row = con.execute(sql_select, (id,)).fetchone()
            club_application = ClubApplication(
                id=row[0],
                title=row[1],
                head=row[2],
                description=row[3]
            )
            return club_application

    def findAllClubApplications(self):
        club_application = []
        with con:
            sql_select = """SELECT 
                                       id,
                                       title,
                                       head,
                                       description
                                    FROM club_applications"""
            raw_applications = con.execute(sql_select).fetchall()
            for row in raw_applications:
                application = ClubApplication(
                    id=row[0],
                    title=row[1],
                    head=row[2],
                    description=row[3])
                club_application.append(application)

        return club_application

    def addClubApplication(self, application_object: ClubApplication):
        with con:
            sql_insert = """INSERT INTO club_applications (title, head, description) 
                            VALUES (?, ?, ?)"""
            con.execute(sql_insert, (application_object.title,
                                     application_object.head,
                                     application_object.description))
            return {"message": "Заявка отправлена."}

    def updateClubApplication(self, id, application_object:ClubApplication):
        with con:
            sql_update = """UPDATE 
                              club_applications
                            SET
                              title = ?,
                              head = ?,
                              description = ?,
                            WHERE
                              id = ?"""

            con.execute(sql_update, (application_object.title,
                                     application_object.head,
                                     application_object.description,
                                     id))

    def deleteClubApplication(self, club_application_id):
        with con:
            sql_delete = """DELETE FROM club_applications WHERE id = ?"""
            con.execute(sql_delete, (club_application_id,))
