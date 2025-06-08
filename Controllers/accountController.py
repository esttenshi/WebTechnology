from flask import jsonify, request, redirect, url_for, session, render_template
from flask_restful import Resource
from Models.account import Account
from Services.accountService import AccountService
from Services.userService import UserService
from application import app

_accountService = AccountService()
_userService = UserService()
app.secret_key = 'secret'

def login_user(user_status, user_id, user_clubs):

    """
    Сохраняет сессию аккаунта
    """
    if user_status == 'Администратор':
        session['user_logged'] = 1
        session['user_status'] = 0
    else:
        session['user_logged'] = 1
        session['user_status'] = user_status
        session['user_id'] = user_id
        session['user_clubs'] = user_clubs

def isLogged():

    """
    Проверяет сессию аккаунта
    """

    return True if session.get('user_logged') else False

def logoutUser():

    """
    Удаляет сессию аккаунта
    """
    if session['user_status'] != 0:
        session.pop('user_logged', None)
        session.pop('user_status', None)
        session.pop('user_id', None)
        session.pop('user_clubs', None)
    else:
        session.pop('user_logged', None)
        session.pop('user_status', None)

class AccountController(Resource):

    """
    Класс контроллера для работы с аккаунтом
    
    ...
    
    Атрибуты
    ---------
    _accountService : AccountService
        Сервис для работы с аккаунтом
    _userService: UserService
        Сервис для работы с пользователями

    Методы
    ------
    registration()
        Регистрирует аккаунт
    login()
        Аутентифицирует аккаунт
    logout()
        Выход из аккаунта
    get_account(id = None)
        Возвращает аккаунт по идентификатору
    delete_account(id)
        Удаляет аккаунт по идентификатору
    add_account()
        Добавляет аккаунт
    update_account(id)
        Обновляет информацию об аккаунте по идентификатору
    """

    @staticmethod
    @app.route('/registration', methods=['POST'])
    def registration():

        """
        Регистрирует аккаунт
        
        Параметры
        ---------
        login : str
            Логин аккаунта
        password : str
            Пароль аккаунта
        confirm_password : str
            Подтверждение пароля аккаунта

        Возвращает
        ---------
        redirect(url_for('get_main_page'))
            Перенаправление на главную страницу
        """

        login = request.json.get('login')
        password = request.json.get('password')
        confirm_password = request.json.get('confirm_password')

        if not login or not password or not confirm_password:
            return jsonify({'Сообщение': 'Заполните все поля'}), 400

        if password != confirm_password:
            return jsonify({'Сообщение': 'Пароли не совпадают'}), 400

        existing_account = _accountService.findAccount(login)
        if existing_account:
            return jsonify({'Сообщение': 'Такой логин уже существует'}), 400

        new_account = Account(login=login, password=password)
        _accountService.registration(new_account)
        login_user()
        return redirect(url_for('get_main_page'))

    @staticmethod
    @app.route('/login', methods=['POST'])
    @app.route('/main.html')
    def login():

        """
        Аутентифицирует аккаунт
        
        Параметры
        ---------
        login : str
            Логин аккаунта
        password : str
            Пароль аккаунта

        Возвращает
        ---------
        redirect(url_for('get_main_page'))
            Перенаправление на главную страницу
        """

        login = request.json.get('login')
        password = request.json.get('password')

        if not login or not password:
            return jsonify({'Сообщение': 'Заполните все поля'}), 400

        account = _accountService.authenticate_account(login, password)
        if account:
            user = _userService.findUser(account.id)
            login_user(user.status, user.id, user.clubs)
            return redirect(url_for('get_main_page'))
        else:
            return jsonify({'Сообщение': 'Некорректный логин или пароль'}), 400

    @staticmethod
    @app.route('/logout', methods=['GET'])
    def logout():

        """
        Выход из аккаунта

        Параметры
        ---------
        login : str
            Логин аккаунта
        password : str  
            Пароль аккаунта

        Возвращает
        ---------
        redirect(url_for('get_entry_page'))
            Перенаправление на страницу входа
        """

        if not isLogged():
            return redirect(url_for('get_entry_page'))

        logoutUser()

        return redirect(url_for('get_entry_page'))

    @staticmethod
    @app.route('/accounts', methods=['GET'])
    def get_accounts():

        """
        Возвращает список аккаунтов

        Возвращает
        ---------
        jsonify({"accounts": _accountService.findAllAccounts()})
            Список аккаунтов
        """

        return jsonify({"accounts": _accountService.findAllAccounts()})

    @staticmethod
    @app.route('/accounts/<int:id>', methods=['GET'])
    def get_account(id):

        """
        Возвращает аккаунт по идентификатору

        Параметры
        ---------
        id : int
            Идентификатор аккаунта

        Возвращает
        ---------
        jsonify(account)
            Аккаунт
        """

        account = _accountService.findAccount(id)
        return jsonify(account)

    @staticmethod
    @app.route('/accounts/<int:id>', methods=['DELETE'])
    def delete_account(id):

        """
        Удаляет аккаунт по идентификатору

        Параметры
        ---------
        id : int
            Идентификатор аккаунта

        Возвращает
        ---------
        jsonify(id)
            Идентификатор аккаунта
        """

        _accountService.deleteAccount(id)
        return jsonify(id)

    @staticmethod
    @app.route('/accounts/<int:id>', methods=['PUT'])
    def update_account(id):

        """
        Обновляет аккаунт по идентификатору

        Параметры
        ---------
        id : int
            Идентификатор аккаунта
        login : str
            Логин аккаунта
        password : str
            Пароль аккаунта

        Возвращает  
        ---------
        jsonify({"users": _accountService.findAllAccounts()})
            Список аккаунтов
        """
        
        request_data = request.get_json()
        account = Account(
            login=request_data["login"],
            password=request_data["password"])
        _accountService.updateAccount(id, account)
        return jsonify({"users": _accountService.findAllAccounts()})

