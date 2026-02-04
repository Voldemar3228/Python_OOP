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


def test_audit_and_risk_analyzer():
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
    audit_log = AuditLog('AuditLog_Day5_2')
    new_processor.add_AuditLog(audit_log)
    # Добавление модуля анализа риска к транзакционному процессору
    risk_analyzer = RiskAnalyzer()
    new_processor.add_RiskAnalyzer(risk_analyzer)
    # Добавление банков в работу процессора
    new_processor.add_bank(new_bank)
    new_processor.add_bank(old_bank)
    # Создание очереди транзакций
    new_processor.add_transaction_in_queue('qwer', None, 'qqq',
                                           'deposit', 1000, 'RUB')
    new_processor.add_transaction_in_queue('qwer2', None, 'qqq',
                                           'deposit', 10000, 'RUB')
    new_processor.add_transaction_in_queue('qwer3', None, 'mmm',
                                           'deposit', 10000, 'RUB')
    new_processor.add_transaction_in_queue('qwer4', None, 'mmm',
                                           'deposit', 10000, 'RUB')
    new_processor.add_transaction_in_queue('qwer5', None, 'mmm',
                                           'deposit', 10000, 'RUB')
    new_processor.add_transaction_in_queue('qwer6', None, 'mmm',
                                           'deposit', 10000, 'RUB')
    new_processor.add_transaction_in_queue('qwer7', None, 'mmm',
                                           'deposit', 10000, 'RUB')
    new_processor.add_transaction_in_queue('qwer8', None, 'mmm',
                                           'deposit', 10000, 'RUB')
    new_processor.add_transaction_in_queue('qwer9', None, 'mmm',
                                           'deposit', 10000, 'RUB')
    new_processor.add_transaction_in_queue('qwer10', 'mmm', 'qqq',
                                           'deposit', 100, 'RUB', queue_priority=5)
    new_processor.add_transaction_in_queue('qwer11', 'qqq', 'mmm',
                                           'withdraw', 2, 'USD')

    # Запуск очереди транзакций
    new_processor.apply_transaction()

    # Информация по работе транзакционного процессора
    new_processor.__str__()

    # Работа Аудита
    print(audit_log.summary_audit())

    # Сортировка по важности логов
    audit_log.filtration('severity')
    # audit_log.filtration('Type')
    # audit_log.filtration('asdf')


test_audit_and_risk_analyzer()

