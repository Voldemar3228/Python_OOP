import abc
import datetime
import random  # для генерации UUID
import string  # для генерации UUID
from datetime import datetime, time, timedelta  # для проверки временных промежутков
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
    # , Transaction     # класс транзакции
    # , TransactionQueue    # класс очереди транзакции
    , TransactionProcessor  # класс транзакционного процессора
    , AuditLog  # класс Аудита
    , RiskAnalyzer  # класс Анализатора риска
)


def test_transaction_proccessor():
    # Создание Банка
    new_bank = Bank('Новый банк')
    old_bank = Bank('Старый банк')
    # Создание клиентов:
    #   - нового банка
    print(new_bank.add_client('Сидоров Сан Саныч', 'qwer', '738923 dj@jd.com', '12.03.2005', 111))
    print(new_bank.add_client('Иванов Иван Иванович', 'asdf', '738923 dj@jd.com', '12.03.2005', 222))
    print(new_bank.add_client('Петров Петр Петрович', 'zxcv', '738923 dj@jd.com', '12.03.2005', 333))
    #   - старого банка
    print(old_bank.add_client('Петров Петр Петрович', 'poiu', '738923 dj@jd.com', '12.03.2005', 444))
    # Открытие счетов для 'qwer' (новый банк)
    new_bank.open_account('SavingsAccount', 'qqq', 'qwer', 'RUB')
    new_bank.open_account('SavingsAccount', 'www', 'qwer', 'RUB')
    # Открытие счетов для 'asdf'. (новый банк)
    new_bank.open_account('PremiumAccount', 'sss', 'asdf', 'RUB')
    # Открытие счетов для 'zxcv'. (новый банк)
    new_bank.open_account('InvestmentAccount', 'ccc', 'zxcv', 'RUB')
    # Открытие счетов для 'poiu' (старый банк)
    old_bank.open_account('SavingsAccount', 'mmm', 'poiu', 'RUB')
    # Создание транзакционного процессора
    new_processor = TransactionProcessor()
    # Добавление модуля аудита к транзакционному процессору
    audit_log = AuditLog('AuditLog_Day5_1')
    new_processor.add_AuditLog(audit_log)
    # Добавление модуля анализа риска к транзакционному процессору
    risk_analyzer = RiskAnalyzer()
    new_processor.add_RiskAnalyzer(risk_analyzer)
    # Добавление банков в работу процессора
    new_processor.add_bank(new_bank)
    new_processor.add_bank(old_bank)
    # Создание очереди транзакций
    new_processor.add_transaction_in_queue('num1', None, 'qqq',
                                           'deposit', 100000, 'RUB', queue_priority=1)
    new_processor.add_transaction_in_queue('num2', None, 'www',
                                           'deposit', 100000, 'RUB', queue_priority=1)
    new_processor.add_transaction_in_queue('num3', 'sss', None,
                                           'deposit', 150000, 'RUB', queue_priority=1)
    new_processor.add_transaction_in_queue('num4', 'ccc', None,
                                           'deposit', 200000, 'RUB', queue_priority=1)
    new_processor.add_transaction_in_queue('num5', None, 'mmm',
                                           'deposit', 250000, 'RUB', queue_priority=1)
    # Отмена транзакции
    new_processor.set_transaction_to_cancel('num2')
    # Проверка конвертации валюты и отложенной операции
    new_processor.add_transaction_in_queue('num6', 'qqq', 'sss',
                                           'withdraw', 1, 'USD', "20.12.2026")
    # Проверка внешней операции
    new_processor.add_transaction_in_queue('num7', 'qqq', 'mmm',
                                           'deposit', 2, 'USD')
    # Проверка InvestmentAccount

    new_processor.add_transaction_in_queue('num8', 'ccc', None,
                                           'deposit', 1, 'USD', "etf", "20.12.2026", queue_priority=3)
    new_processor.add_transaction_in_queue('num9', 'ccc', None,
                                           'deposit_securities', 10, 'USD', "etf", "20.12.2026", queue_priority=4)
    new_processor.add_transaction_in_queue('num10', 'ccc', None,
                                           'withdraw_securities', 4, 'CNY', "etf", "20.12.2026", queue_priority=5)
    # Проверка невыполненных транзакций
    new_processor.add_transaction_in_queue('num11', None, 'www',
                                           'deposit', 500000, 'RUB', queue_priority=5)
    new_processor.add_transaction_in_queue('num12', None, 'www',
                                           'depositqwer', 500000, 'RUB', queue_priority=5)
    new_processor.add_transaction_in_queue('num13', None, 'qqq',
                                           'withdraw', 200000, 'RUB', queue_priority=5)
    # Запуск очереди транзакций
    new_processor.apply_transaction()

    # Работа Аудита
    print(audit_log.summary_audit())

    # Команды для проверки статуса счета (можно вставлять до запуска очереди транзакций и после)
    # new_bank.search_accounts('qqq')
    # new_bank.search_accounts('www')
    # new_bank.search_accounts('sss')
    # new_bank.search_accounts('ссс')
    # old_bank.search_accounts('mmm')

    # Информация по работе транзакционного процессора
    new_processor.__str__()








test_transaction_proccessor()

