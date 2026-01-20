import abc
import datetime
import random  # для генерации UUID
import string  # для генерации UUID
from datetime import datetime, time  # для проверки временных промежутков
from abc import ABC, abstractmethod  # Импортируем необходимые модули для создания абстрактного класса


from bank import (
    # AccountFrozenError  # Ошибка: нельзя снять или пополнить счет, у которого статус "замороженный"
    # , AccountClosedError    # Ошибка: нельзя снять или пополнить счет, у которого статус "закрытый"
    # , InvalidOperationError  # Ошибка недопустимости операции
    # , InsufficientFundsError    # Ошибка недостаточности средств
    # , AbstractAccount   # Абстрактный класс счета
    # , BankAccount   # Банковский класс счета
    # , SavingsAccount    # Накопительный счет / вклад
    # , PremiumAccount    # Премиум счет
    # , InvestmentAccount     # Инвестиционный счет
     Bank  # класс банка
    # , Client    # класс клиента
    # , Bank_Client_card    # класс карточки клиента
)


def test_Bank_system():
    # Создание Банка
    new_bank = Bank('Новый банк')
    # Создание клиентов
    print(new_bank.add_client('Сидоров Сан Саныч', 'qwer', '738923 dj@jd.com', '12.03.2005', 111))
    print(new_bank.add_client('Иванов Иван Иванович', 'asdf', '738923 dj@jd.com', '12.03.2005', 222))
    print(new_bank.add_client('Петров Петр Петрович', 'zxcv', '738923 dj@jd.com', '12.03.2005', 333))
    # Открытие счетов для 'qwer'
    new_bank.open_account('SavingsAccount', 'qqq', 'qwer', 'RUB')
    new_bank.open_account('SavingsAccount', 'www', 'qwer', 'RUB')
    # Открытие счетов для 'asdf'.
    new_bank.open_account('PremiumAccount', 'sss', 'asdf', 'RUB')
    # Открытие счетов для 'zxcv'.
    new_bank.open_account('InvestmentAccount', 'ccc', 'zxcv', 'RUB')
    # Пароль 333. Введите неправильный пароль, чтобы вызвать заморозку клиента и проверить операции по его счетам
    new_bank.transaction('qqq', 'deposit', 20000)
    new_bank.transaction('qqq', 'deposit', 20000)
    new_bank.transaction('www', 'deposit', 20000)
    # Разморозка клиента qwer - он станет активным. Проверка операции со счетами
    new_bank.unfreeze_client('qwer')
    new_bank.transaction('qqq', 'deposit', 20000)
    new_bank.transaction('www', 'deposit', 20000)
    # Вызов заморозки счета qqq и проверка операции со счетами
    new_bank.freeze_account('qqq')
    # new_bank.transaction('qqq', 'deposit', 20000)
    # Закомментируйте предыдущую строку "new_bank.transaction('qqq', 'deposit', 20000) ". Проверка разморозки счета
    new_bank.unfreeze_account('qqq')
    new_bank.transaction('qqq', 'deposit', 20000)
    # Закрытие счета 'qqq'. Дальнейшие операции по нему невозможны.
    new_bank.close_account('qqq')
    new_bank.transaction('www', 'deposit', 20000)
    # Закрытие клиента 'qwer'. Дальнейшие операции по его счетам qqq и www невозможны.
    new_bank.close_client('qwer')
    new_bank.transaction('www', 'deposit', 20000)
    # Переключение на нового клиента 'asdf'
    new_bank.authenticate_client('asdf', 222)
    new_bank.transaction('sss', 'deposit', 30000)
    # Заморозка счета через подозрительные действия SUSPICIOUS_SUM.
    new_bank.transaction('sss', 'deposit', 3000000)
    new_bank.show_all_clients()

    # Информация о банке
    new_bank.__str__()
    new_bank.show_all_clients()

    # Проверка метода get_total_balance #
    # Баланс банка
    new_bank.get_total_balance()
    # Баланс конкретного пользователя по ID
    new_bank.get_total_balance('asdf')
    # Баланс несуществующего пользователя
    new_bank.get_total_balance('asdfzxcv')

    # Проверка get_clients_ranking
    new_bank.get_clients_ranking()


test_Bank_system()

