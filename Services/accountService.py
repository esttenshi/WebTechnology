from application import con
from Models.account import Account

class AccountService:

    """
    Класс для работы с аккаунтами

    ...

    Атрибуты
    -------
    id : int
        Идентификатор аккаунта
    login : str
        Логин аккаунта
    password : str
        Пароль аккаунта

    Методы
    ------
    registration
        Регистрация аккаунта
    authenticate_account
        Аутентификация аккаунта
    findAccount
        Находит аккаунт по идентификатору
    findAllAccounts
        Возвращает список аккаунтов
    deleteAccount
        Удаляет аккаунт по идентификатору
    updateAccount
        Обновляет аккаунт по идентификатору
    """

    def registration(self, user_object: Account):

        """
        Регистрация аккаунта

        Параметры
        ---------
        login : str
            Логин аккаунта
        password : str
            Пароль аккаунта

        Возвращает
        ---------
        None
        """

        with con:
            sql_insert_accounts = """INSERT INTO 
                                        accounts
                                        (login, 
                                        password
                                        ) 
                                    VALUES 
                                        (?,
                                         ?)"""
            con.execute(sql_insert_accounts, (user_object.login, user_object.password))
            last_id = con.execute("SELECT last_insert_rowid()").fetchone()[0]
            sql_insert_users = """INSERT INTO 
                                    users
                                    (id) 
                                  VALUES 
                                    (?)"""
            con.execute(sql_insert_users, (last_id,))

    def authenticate_account(self, login, password):

        """
        Аутентификация аккаунта

        Параметры
        ---------
        login : str
            Логин аккаунта
        password : str
            Пароль аккаунта

        Возвращает
        ---------
        None
        """

        with con:
            sql_select = """SELECT 
                                id, 
                                login, 
                                password
                            FROM 
                                accounts
                            WHERE 
                                login = ? 
                            AND 
                                password = ?"""
            account_data = con.execute(sql_select, (login, password)).fetchone()
            if account_data:
                return Account(id=account_data[0], login=account_data[1], password=account_data[2])
            else:
                return None

    def findAccount(self, id):

        """
        Находит аккаунт по идентификатору

        Параметры
        ---------
        id : int
            Идентификатор аккаунта

        Возвращает
        ---------
        account : Account
            Аккаунт
        """

        with con:
            sql_select = """SELECT 
                               id,
                               login,
                               password
                            FROM accounts
                            WHERE id = ?"""
            raw_account = con.execute(sql_select, (id,)).fetchone()
            if raw_account:
                account = Account(
                    id=raw_account[0],
                    login=raw_account[1],
                    password=raw_account[2],
                )
                return account
            else:
                return None

    def findAllAccounts(self):

        """
        Возвращает список аккаунтов

        Возвращает
        ---------
        accounts : list
            Список аккаунтов
        """

        accounts = []
        with con:
            sql_select = """SELECT 
                               id,
                               login,
                               password
                            FROM accounts"""
            raw_accounts = con.execute(sql_select).fetchall()
            for row in raw_accounts:
                account = Account(
                    id=row[0],
                    login=row[1],
                    password=row[2])
                accounts.append(account)
        return accounts

    def deleteAccount(self, id):

        """
        Удаляет аккаунт по идентификатору

        Параметры
        ---------
        id : int
            Идентификатор аккаунта

        Возвращает
        ---------
        None
        """

        with con:
            sql_delete_accounts = """DELETE FROM accounts WHERE id = ?"""
            con.execute(sql_delete_accounts, (id,))

            sql_delete_users = """DELETE FROM users WHERE id = ?"""
            con.execute(sql_delete_users, (id,))

    def updateAccount(self, id, user_object: Account):

        """
        Обновляет аккаунт по идентификатору

        Параметры
        ---------
        id : int
            Идентификатор аккаунта
        user_object : Account
            Объект аккаунта

        Возвращает
        ---------
        None
        """
        
        with con:
            sql_update = """UPDATE accounts
                            SET
                              login = ?,
                              password = ?
                            WHERE
                              id = ?"""
            con.execute(sql_update, (user_object.login,
                                     user_object.password,
                                     id))