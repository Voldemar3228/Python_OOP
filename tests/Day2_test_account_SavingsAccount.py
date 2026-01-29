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
