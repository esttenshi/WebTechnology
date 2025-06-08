from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['database.db'] = 'sqlite:///applications.db'
db = SQLAlchemy(app)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.String(100))
    group = db.Column(db.String(100))
    status = db.Column(db.String(10))

@app.route('/accept_application', methods=['POST'])
def accept_application():
    application_id = request.form['application_id']
    application = Application.query.get(application_id)
    application.status = 'accepted'
    db.session.commit()
    return 'Application accepted'

@app.route('/reject_application', methods=['POST'])
def reject_application():
    application_id = request.form['application_id']
    application = Application.query.get(application_id)
    application.status = 'rejected'
    db.session.commit()
    return 'Application rejected'

@app.route('/applications')
def applications():
    applications = Application.query.all()
    return render_template('applications.html', applications=applications)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)