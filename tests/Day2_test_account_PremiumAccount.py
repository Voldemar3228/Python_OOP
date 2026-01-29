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


def test_account_PremiumAccount():
    # Создание Банка
    new_bank = Bank('Новый банк')
    # Создание клиентов
    print(new_bank.add_client('Сидоров Сан Саныч', 'qwer', '738923 dj@jd.com', '12.03.2005', 111))
    # Проверка PremiumAccount #
    print(new_bank.open_account('PremiumAccount', 'eee', 'qwer', 'RUB'))
    # Операции с PremiumAccount
    new_bank.transaction('eee', '__str__')
    # Пополнение счета
    new_bank.transaction('eee', 'deposit', 220000)
    new_bank.transaction('eee', '__str__')
    # Снятие со счета
    new_bank.transaction('eee', 'withdraw', 50000)
    new_bank.transaction('eee', '__str__')
    # Снятие со счета в долг
    new_bank.transaction('eee', 'withdraw', 200000)
    new_bank.transaction('eee', '__str__')
    # Пополнение с погашением долга
    new_bank.transaction('eee', 'deposit', 50000)
    new_bank.transaction('eee', '__str__')
    # Снятие сверх лимита
    # new_bank.transaction('eee', 'withdraw', 200000)
    new_bank.transaction('eee', 'get_account_info')


test_account_PremiumAccount()

