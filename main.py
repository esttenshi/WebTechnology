from application import app, api
from Controllers.accountController import AccountController
from Controllers.userController import UserController
from Controllers.clubController import ClubController
from Controllers.statusController import StatusController
from Controllers.pageController import PageController
from Controllers.newsController import NewsController
from Controllers.applicationController import ApplicationController
from Controllers.clubApplicationController import ClubApplicationController
from Controllers.eventController import EventController

if __name__ == '__main__':
    api.add_resource(AccountController, '/accounts')
    api.add_resource(UserController, '/users')
    api.add_resource(NewsController, '/news')
    api.add_resource(ClubController, '/clubs')
    api.add_resource(StatusController, '/status')
    api.add_resource(PageController, '/main')
    api.add_resource(ApplicationController, '/applications')
    api.add_resource(ClubApplicationController, '/club_applications')
    api.add_resource(EventController, '/add_event')
    app.run(debug=True, port=3000, host="127.0.0.1")
