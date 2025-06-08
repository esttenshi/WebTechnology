from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['database.db'] = 'sqlite:///club_applications.db'
db = SQLAlchemy(app)

class ClubApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(10))

@app.route('/accept_club_application', methods=['POST'])
def accept_club_application():
    club_application_id = request.form['club_application_id']
    club_application = ClubApplication.query.get(club_application_id)
    club_application.status = 'accepted'
    db.session.commit()
    return 'Application accepted'

@app.route('/reject_club_application', methods=['POST'])
def reject_application():
    club_application_id = request.form['club_application_id']
    club_application = ClubApplication.query.get(club_application_id)
    club_application.status = 'rejected'
    db.session.commit()
    return 'Application rejected'

@app.route('/club_applications')
def clubApplications():
    club_applications = ClubApplication.query.all()
    return render_template('club_applications.html', club_applications=club_applications)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)