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


def test_account_SavingsAccount():
    # Создание Банка
    new_bank = Bank('Новый банк')
    # Создание клиентов
    print(new_bank.add_client('Сидоров Сан Саныч', 'qwer', '738923 dj@jd.com', '12.03.2005', 111))
    # Открытие счетов для 'qwer'
    new_bank.open_account('SavingsAccount', 'qqq', 'qwer', 'RUB')
    new_bank.open_account('SavingsAccount', 'www', 'qwer', 'RUB')
    # Операции со счетом SavingsAccount
    new_bank.transaction('qqq', 'deposit', 20000)
    new_bank.transaction('qqq', '__str__', 20000)
    new_bank.transaction('qqq', 'withdraw', 10000)
    new_bank.transaction('qqq', '__str__')
    new_bank.transaction('qqq', 'apply_monthly_interest')
    new_bank.transaction('qqq', 'get_account_info')


test_account_SavingsAccount()

# ================================================================ #
# ========================= Тестирование ========================= #
# ================================================================ #
# # Создание Банка
# new_bank = Bank('Новый банк')
# # Создание клиентов
# print(new_bank.add_client('Сидоров Сан Саныч', 'qwer', '738923 dj@jd.com', '12.03.2005', 111))
# print(new_bank.add_client('Иванов Иван Иванович', 'asdf', '738923 dj@jd.com', '12.03.2005', 222))
# print(new_bank.add_client('Петров Петр Петрович', 'zxcv', '738923 dj@jd.com', '12.03.2005', 333))
# # Открытие счетов для 'qwer'
# new_bank.open_account('SavingsAccount', 'qqq', 'qwer', 'RUB')
# new_bank.open_account('SavingsAccount', 'www', 'qwer', 'RUB')
# # Открытие счетов для 'asdf'.
# new_bank.open_account('PremiumAccount', 'sss', 'asdf', 'RUB')
# # Открытие счетов для 'zxcv'.
# new_bank.open_account('InvestmentAccount', 'ccc', 'zxcv', 'RUB')
# # Пароль 333. Введите неправильный пароль, чтобы вызвать заморозку клиента и проверить операции по его счетам
# new_bank.transaction('qqq', 'deposit', 20000)
# new_bank.transaction('qqq', 'deposit', 20000)
# new_bank.transaction('www', 'deposit', 20000)
# # Разморозка клиента qwer - он станет активным. Проверка операции со счетами
# new_bank.unfreeze_client('qwer')
# new_bank.transaction('qqq', 'deposit', 20000)
# new_bank.transaction('www', 'deposit', 20000)
# # Вызов заморозки счета qqq и проверка операции со счетами
# new_bank.freeze_account('qqq')
# # new_bank.transaction('qqq', 'deposit', 20000)
# # Закомментируйте предыдущую строку "new_bank.transaction('qqq', 'deposit', 20000) ". Проверка разморозки счета
# new_bank.unfreeze_account('qqq')
# new_bank.transaction('qqq', 'deposit', 20000)
# # Закрытие счета 'qqq'. Дальнейшие операции по нему невозможны.
# new_bank.close_account('qqq')
# new_bank.transaction('www', 'deposit', 20000)
# # Закрытие клиента 'qwer'. Дальнейшие операции по его счетам qqq и www невозможны.
# new_bank.close_client('qwer')
# new_bank.transaction('www', 'deposit', 20000)
# # Заморозка счета через подозрительные действия SUSPICIOUS_SUM. Пароль 222
# new_bank.transaction('sss', 'deposit', 3000000)
# # new_bank.transaction('sss', 'deposit', 3000)
# # Закомментируйте строку "new_bank.transaction('sss', 'deposit', 3000)". Проверка разморозки счета
# new_bank.unfreeze_account('sss')
# new_bank.transaction('sss', 'deposit', 20000)

# =============================================================================== #
# ========================= Дополнительное тестирование ========================= #
# =============================================================================== #
# Закомментируйте предыдущий блок "Тестирование"

########################## Проверка транзакций ############################
# # Создание Банка и клиентов #
# new_bank = Bank('Новый банк')
# print(new_bank.add_client('Сидоров Сан Саныч', 'asdf', '738923 dj@jd.com', '12.03.2005', 222))
# print(new_bank.add_client('Иванов Иван Иванович', 'qwer', '738923 dj@jd.com', '12.03.2005', 111))
# # ======================= #
# # ======================= #
# # Проверка SavingsAccount #
# new_bank.open_account('SavingsAccount', 'qqq', 'qwer', 'RUB')
# new_bank.transaction('qqq', 'deposit', 20000)
# new_bank.transaction('qqq', '__str__', 20000)
# new_bank.transaction('qqq', 'withdraw', 10000)
# new_bank.transaction('qqq', '__str__')
# new_bank.transaction('qqq', 'apply_monthly_interest')
# new_bank.transaction('qqq', 'get_account_info')
# # ======================= #
# # ======================= #
# # Проверка PremiumAccount #
# print(new_bank.open_account('PremiumAccount', 'eee', 'qwer', 'RUB'))
# # Операции с PremiumAccount
# new_bank.transaction('eee', '__str__')
# # Пополнение счета
# new_bank.transaction('eee', 'deposit', 220000)
# new_bank.transaction('eee', '__str__')
# # Снятие со счета
# new_bank.transaction('eee', 'withdraw', 50000)
# new_bank.transaction('eee', '__str__')
# # Снятие со счета в долг
# new_bank.transaction('eee', 'withdraw', 200000)
# new_bank.transaction('eee', '__str__')
# # Пополнение с погашением долга
# new_bank.transaction('eee', 'deposit', 50000)
# new_bank.transaction('eee', '__str__')
# # Снятие сверх лимита
# # new_bank.transaction('eee', 'withdraw', 200000)
# new_bank.transaction('eee', 'get_account_info')
# # ======================= #
# # ======================= #
# # Создание InvestmentAccount
# print(new_bank.open_account('InvestmentAccount', 'rrr', 'qwer', 'RUB'))
# # Операции с InvestmentAccount
# new_bank.transaction('rrr', '__str__')
# # пополнение счета
# new_bank.transaction('rrr', 'deposit', 200000)
# new_bank.transaction('rrr', '__str__')
# # покупка бумаг
# new_bank.transaction('rrr', 'deposit_securities', 'stocks', 20000)
# new_bank.transaction('rrr', 'deposit_securities', 'bonds', 20000)
# new_bank.transaction('rrr', 'deposit_securities', 'etf', 20000)
# new_bank.transaction('rrr', '__str__')
# # продажа бумаг
# new_bank.transaction('rrr', 'withdraw_securities', 'stocks', 10000)
# new_bank.transaction('rrr', 'withdraw_securities', 'bonds', 20000)
# new_bank.transaction('rrr', 'withdraw_securities', 'etf', 10000)
# new_bank.transaction('rrr', '__str__')
# # снятие со счета
# new_bank.transaction('rrr', 'withdraw', 50000)
# new_bank.transaction('rrr', '__str__')
# # Рост ценных бумаг
# new_bank.transaction('rrr', 'project_yearly_growth')
# new_bank.transaction('rrr', '__str__')
# # # Недостаточно средств
# # new_bank.transaction('rrr', 'deposit_securities', 'stocks', 200000)
# # new_bank.transaction('rrr', '__str__')
# # # Неправильные бумаги
# # new_bank.transaction('rrr', 'deposit_securities', 'stocksss', 100000)
# # new_bank.transaction('rrr', '__str__')
# # # Продажа несуществующей бумаги
# # new_bank.transaction('rrr', 'withdraw_securities', 'etfqwe', 10000)
# # new_bank.transaction('rrr', '__str__')
# # # Вывод недоступной суммы (заморозка аккаунта)
# # new_bank.transaction('rrr', 'withdraw', 5000000)
# # new_bank.transaction('rrr', '__str__')
# # new_bank.transaction('rrr', 'withdraw', 5000)
# # new_bank.transaction('rrr', '__str__')

# # ======================= #
# # Операция с другим пользователем (пароль 222)
# # ======================= #
# new_bank.open_account('SavingsAccount', 'aaa', 'asdf', 'RUB')
# new_bank.transaction('aaa', 'deposit', 20000)
# new_bank.transaction('aaa', '__str__', 20000)
# # ======================= #
# # Операция с начальным пользователем (пароль 111)
# new_bank.transaction('rrr', 'deposit', 200000)
# new_bank.transaction('rrr', '__str__')
# # ======================= #
# new_bank.__str__()
# new_bank.show_all_clients()

# # Проверка метода get_total_balance #
# # Баланс банка
# new_bank.get_total_balance()
# # Баланс конкретного пользователя по ID
# new_bank.get_total_balance('asdf')
# # Баланс несуществующего пользователя
# new_bank.get_total_balance('asdfzxcv')

# # Проверка get_clients_ranking
# new_bank.get_clients_ranking()
