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
    print(new_bank.add_client('Макаров Макар Макарович', 'poiu', '738923 dj@jd.com', '12.03.2005', 444))
    print(new_bank.add_client('Петров Петр Петрович', 'lkjh', '738923 dj@jd.com', '12.03.2005', 555))
    #   - старого банка
    print(old_bank.add_client('Азаматов Азамат Азаматович', 'rewq', '738923 dj@jd.com', '12.03.2005', 666))
    print(old_bank.add_client('Княжева Княжна Императоровна', 'fdsa', '738923 dj@jd.com', '12.03.2005', 777))
    print(old_bank.add_client('Николаев Николай Николаевич', 'vcxz', '738923 dj@jd.com', '12.03.2005', 888))
    print(old_bank.add_client('Дронов Дрон Дроныч', 'uiop', '738923 dj@jd.com', '12.03.2005', 999))
    print(old_bank.add_client('Каров Кар Карыч', 'hjkl', '738923 dj@jd.com', '12.03.2005', 000))

    # Открытие счетов (новый банк)
    new_bank.open_account('SavingsAccount', 'qqq', 'qwer', 'RUB')
    new_bank.open_account('SavingsAccount', 'www', 'asdf', 'USD')
    new_bank.open_account('PremiumAccount', 'eee', 'zxcv', 'EUR')
    new_bank.open_account('PremiumAccount', 'rrr', 'poiu', 'KZT')
    new_bank.open_account('InvestmentAccount', 'ttt', 'lkjh', 'CNY')
    # Открытие счетов (старый банк)
    old_bank.open_account('SavingsAccount', 'aaa', 'rewq', 'CNY')
    old_bank.open_account('SavingsAccount', 'sss', 'fdsa', 'KZT')
    old_bank.open_account('PremiumAccount', 'ddd', 'vcxz', 'EUR')
    old_bank.open_account('PremiumAccount', 'fff', 'uiop', 'USD')
    old_bank.open_account('InvestmentAccount', 'ggg', 'hjkl', 'RUB')


    # Создание транзакционного процессора
    new_processor = TransactionProcessor()
    # Добавление модуля аудита к транзакционному процессору
    audit_log = AuditLog('AuditLog_Day6')
    new_processor.add_AuditLog(audit_log)
    # Добавление модуля анализа риска к транзакционному процессору
    risk_analyzer = RiskAnalyzer()
    new_processor.add_RiskAnalyzer(risk_analyzer)
    # Добавление банков в работу процессора
    new_processor.add_bank(new_bank)
    new_processor.add_bank(old_bank)
    # Создание очереди транзакций 1/2
    new_processor.add_transaction_in_queue('num1', None, 'qqq',
                                           'deposit', 100000, 'RUB', queue_priority=1)
    new_processor.add_transaction_in_queue('num2', None, 'www',
                                           'deposit', 100000, 'RUB', queue_priority=1)
    new_processor.add_transaction_in_queue('num3', 'eee', None,
                                           'deposit', 150000, 'RUB', queue_priority=1)
    new_processor.add_transaction_in_queue('num4', 'rrr', None,
                                           'deposit', 200000, 'RUB', queue_priority=1)
    new_processor.add_transaction_in_queue('num5', None, 'ttt',
                                           'deposit', 250000, 'RUB', queue_priority=1)
    new_processor.add_transaction_in_queue('num6', None, 'ttt',
                                           'deposit', 250000, 'RUB', queue_priority=1)
    # Отмена транзакции
    new_processor.set_transaction_to_cancel('num6')
    # Проверка конвертации валюты и отложенной операции
    new_processor.add_transaction_in_queue('num7', 'qqq', 'www',
                                           'withdraw', 1, 'USD', "20.12.2026")
    new_processor.add_transaction_in_queue('num8', 'www', 'eee',
                                           'deposit', 2, 'USD')
    # Проверка InvestmentAccount

    new_processor.add_transaction_in_queue('num9', 'ttt', None,
                                           'deposit', 1, 'USD', "etf", "20.12.2026", queue_priority=3)
    new_processor.add_transaction_in_queue('num10', 'ttt', None,
                                           'deposit_securities', 10, 'USD', "etf", "20.12.2026", queue_priority=4)
    new_processor.add_transaction_in_queue('num11', 'ttt', None,
                                           'withdraw_securities', 4, 'CNY', "etf", "20.12.2026", queue_priority=5)
    # Проверка невыполненных транзакций
    new_processor.add_transaction_in_queue('num12', None, 'www',
                                           'deposit', 500000, 'RUB', queue_priority=5)
    new_processor.add_transaction_in_queue('num13', None, 'www',
                                           'depositqwer', 500000, 'RUB', queue_priority=5)
    new_processor.add_transaction_in_queue('num14', None, 'qqq',
                                           'withdraw', 200000, 'RUB', queue_priority=5)

    # Информация по работе транзакционного процессора (до запуска очереди)
    new_processor.__str__()

    # Запуск очереди транзакций
    new_processor.apply_transaction()

    # Информация по работе транзакционного процессора (после запуска очереди)
    new_processor.__str__()

    # Работа Аудита
    print(audit_log.summary_audit())

    # Сортировка по важности логов
    audit_log.filtration('severity')

    # Создание очереди транзакций 2/2
    new_processor.add_transaction_in_queue('qwer', None, 'aaa',
                                           'deposit', 1000, 'RUB')
    new_processor.add_transaction_in_queue('qwer2', None, 'sss',
                                           'deposit', 10000, 'RUB')
    new_processor.add_transaction_in_queue('qwer3', None, 'ddd',
                                           'deposit', 10000, 'RUB')
    new_processor.add_transaction_in_queue('qwer4', None, 'fff',
                                           'deposit', 10000, 'RUB')
    new_processor.add_transaction_in_queue('qwer5', None, 'ggg',
                                           'deposit', 10000, 'RUB')
    new_processor.add_transaction_in_queue('qwer6', None, 'sss',
                                           'deposit', 10000, 'RUB')
    new_processor.add_transaction_in_queue('qwer7', None, 'sss',
                                           'deposit', 10000, 'RUB')
    new_processor.add_transaction_in_queue('qwer7', None, 'sss',
                                           'deposit', 10000, 'RUB')
    new_processor.add_transaction_in_queue('qwer7', None, 'sss',
                                           'deposit', 10000, 'RUB')
    new_processor.add_transaction_in_queue('qwer8', None, 'sss',
                                           'deposit', 10000, 'RUB')
    new_processor.add_transaction_in_queue('qwer9', None, 'sss',
                                           'deposit', 10000, 'RUB')
    new_processor.add_transaction_in_queue('qwer10', 'sss', 'qqq',
                                           'deposit', 100, 'RUB', queue_priority=5)
    new_processor.add_transaction_in_queue('qwer11', 'sss', 'www',
                                           'withdraw', 2, 'USD')
    new_processor.add_transaction_in_queue('qwer11', 'sss', 'ggg',
                                           'withdraw', 2, 'USD')

    # Запуск очереди транзакций
    new_processor.apply_transaction()

    # Информация по работе транзакционного процессора (после запуска очереди)
    new_processor.__str__()

    # Работа Аудита
    print(audit_log.summary_audit())

    # Сортировка по важности логов
    audit_log.filtration('severity')



    # Команды для проверки статуса счета (можно вставлять до запуска очереди транзакций и после)
    # new_bank.search_accounts('qqq')
    # new_bank.search_accounts('www')
    # new_bank.search_accounts('sss')
    # new_bank.search_accounts('ссс')
    # old_bank.search_accounts('mmm')

    # # Информация по работе транзакционного процессора
    # new_processor.__str__()








test_transaction_proccessor()

