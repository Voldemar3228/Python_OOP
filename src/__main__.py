import abc
import random  # для генерации UUID
import string  # для генерации UUID
from abc import ABC, abstractmethod  # Импортируем необходимые модули для создания абстрактного класса


# Ошибка: нельзя снять или пополнить счет, у которого статус "замороженный"
class AccountFrozenError(Exception):
    def __init__(self, current_status):
        self.current_status = current_status

    def __str__(self):
        return f'Невозможно провести операцию.\n' \
               f'Статус счета: {self.current_status}'


# Ошибка: нельзя снять или пополнить счет, у которого статус "закрытый"
class AccountClosedError(Exception):
    def __init__(self, current_status):
        self.current_status = current_status

    def __str__(self):
        return f'Невозможно провести операцию.\n' \
               f'Статус счета: {self.current_status}'


# Ошибка недопустимости операции: когда не можем выполнить операции снятия и пополнения: неправильные типы данных
class InvalidOperationError(Exception):
    def __init__(self, amount):
        self.amount = amount

    def __str__(self):
        return f'Невозможно выполнить операцию: неправильный тип данных.\n' \
               f'Текущий тип данных у {self.amount}: {type(self.amount)}.\n' \
               f'Требуемый тип данных: {type(1)}.\n'


# Ошибка недостаточности средств - если хотим снять больше того, что есть на счете
class InsufficientFundsError(Exception):
    def __init__(self, withdraw_sum, balance, curr):
        self.withdraw_sum = withdraw_sum
        self.balance = balance
        self.curr = curr

    def __str__(self):
        return f'Недопустимое значение.\n' \
               f'Вы не можете снять {self.withdraw_sum} {self.curr}, ' \
               f'так как сумма больше, чем есть сейчас на счету ({self.balance} {self.curr}).'


class AbstractAccount(abc.ABC):

    def __init__(self, Id, person, secure_balance, status):
        self.Id = Id  # уникальный идентификатор счёта
        self.person = person  # данные владельца
        self.secure_balance = secure_balance  # защищённый баланс
        self.status = status  # статус счёта: активный, замороженный, закрытый

    @abc.abstractmethod
    def deposit(self):
        pass

    def withdraw(self):
        pass

    def get_account_info(self):
        pass


class BankAccount(AbstractAccount, ABC):
    STATUS = ['активный', 'замороженный', 'закрытый', 'Активный', 'Замороженный', 'Закрытый']
    RANDOM_ID_LEN = 6
    CURRENCY_MEANINGS = ['RUB', 'USD', 'EUR', 'KZT', 'CNY']

    def __init__(self, Id, person, secure_balance, status, currency):
        super().__init__(Id, person, secure_balance, status)
        self.currency = currency

    # Валидация ID
    @property
    def Id(self):
        return self._Id

    @Id.setter
    def Id(self, value):
        if not value.strip():
            all_symbols = string.ascii_lowercase + string.digits  # все буквы английского алфавита в нижнем регистре + цифры
            value = ''.join(random.choice(all_symbols) for _ in range(self.RANDOM_ID_LEN))
        self._Id = value

    # Валидация person
    @property
    def person(self):
        return self._person

    @person.setter
    def person(self, value):
        if not value.strip():
            raise ValueError('person have to be not null')
        self._person = value

    # Валидация secure_balance
    @property
    def secure_balance(self):
        return self._secure_balance

    @secure_balance.setter
    def secure_balance(self, value):
        if not str(value).strip():
            raise ValueError('secure_balance should be not null')
        if value < 0:
            raise ValueError("secure_balance can't be negative")
        self._secure_balance = value

    # Валидация status
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if not value.strip():
            raise ValueError('status should be not null')
        self._status = value

    # Валидация currency
    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, value):
        if not value:
            raise ValueError('currency should be not null')
        if value not in self.CURRENCY_MEANINGS:
            raise ValueError('wrong currency')
        self._currency = value

    def validate_operation(self, amount, oper_type):
        if type(amount) is not int:
            raise InvalidOperationError(amount)
        if self.status not in self.STATUS:
            print(f'Статусы могут принимать следующие значения: {self.STATUS}')
            raise ValueError(f'Запрет выполнения операции')
        if self.status in ['замороженный', 'Замороженный']:
            raise AccountFrozenError(self.status)
        if self.status in ['закрытый', 'Закрытый']:
            raise AccountClosedError(self.status)
        if oper_type == 'withdraw' and amount > self.secure_balance:
            raise InsufficientFundsError(amount, self.secure_balance, self.currency)

    def deposit(self, amount):
        self.validate_operation(amount, 'deposit')
        self.secure_balance += amount
        return f'Средства ({amount} {self.currency}) успешно внесены на счет\n'

    def withdraw(self, amount):
        self.validate_operation(amount, 'withdraw')
        self.secure_balance -= amount
        return f'Средства ({amount} {self.currency}) успешно списаны со счета\n'

    def get_account_info(self):
        return f'Уникальный идентификатор счёта: {self.Id}. \n' \
               f'Данные владельца: {self.person}. \n' \
               f'Защищённый баланс: {self.secure_balance}. \n' \
               f'Статус счёта: {self.status}. \n' \
               f'Валюта: {self.currency}. \n'

    def __str__(self):
        id_num = ''
        for i in range(-len(self.Id), 0, 1):
            if i < -4:
                id_num += '*'
            else:
                id_num += self.Id[i]
        self.id_num = id_num
        return f'Тип счёта: BankAccount. \n' \
               f'Владелец: {self.person}. \n' \
               f'Номер счета: {self.id_num}. \n' \
               f'Статус счёта: {self.status}. \n' \
               f'Баланс счета: {self.secure_balance} {self.currency}. \n'


class SavingsAccount(BankAccount):
    def __init__(self, Id, person, secure_balance, status, currency, monthly_rate):
        super().__init__(Id, person, secure_balance, status, currency)
        self.min_balance = secure_balance
        self.monthly_rate = monthly_rate

    @property
    def monthly_rate(self):
        return self._monthly_rate

    @monthly_rate.setter
    def monthly_rate(self, value):
        if not str(value).strip():
            raise ValueError('monthly_rate should be not null')
        if value < 0 or value > 1:
            raise ValueError("monthly_rate have to be between 0 and 1")
        self._monthly_rate = value

    def deposit(self, amount):
        super().deposit(amount)
        return f'Средства ({amount} {self.currency}) успешно внесены на счет\n'

    def withdraw(self, amount):
        super().withdraw(amount)
        self.min_balance = min(self.secure_balance, self.min_balance)
        return f'Средства ({amount} {self.currency}) успешно списаны со счета\n'

    def apply_monthly_interest(self):
        self.secure_balance += self.min_balance * self.monthly_rate
        self.min_balance = self.secure_balance
        return f'Средства ({self.min_balance * self.monthly_rate} {self.currency}) успешно зачислены на счет.\n' \
               f'Текущий баланс: {self.secure_balance}.\n' \
               f'Минимальный остаток: {self.min_balance}'

    def get_account_info(self):
        super().get_account_info()
        return f'Уникальный идентификатор счёта: {self.Id}. \n' \
               f'Данные владельца: {self.person}. \n' \
               f'Защищённый баланс: {self.secure_balance}. \n' \
               f'Статус счёта: {self.status}. \n' \
               f'Минимальный остаток: {self.min_balance}. \n' \
               f'Процентная ставка: {self.monthly_rate}. \n'

    def __str__(self):
        super().__str__()
        return f'Тип счёта: BankAccount. \n' \
               f'Владелец: {self.person}. \n' \
               f'Номер счета: {self.id_num}. \n' \
               f'Статус счёта: {self.status}. \n' \
               f'Баланс счета: {self.secure_balance} {self.currency}. \n' \
               f'Минимальный остаток: {self.min_balance}. \n' \
               f'Процентная ставка: {self.monthly_rate}. \n'


class PremiumAccount(BankAccount):
    def __init__(self, Id, person, secure_balance, status, currency, overdraft_limit, daily_withdraw_limit, fee):
        super().__init__(Id, person, secure_balance, status, currency)
        self.overdraft_limit = overdraft_limit
        self.overdraft_balance = overdraft_limit
        self.daily_withdraw_limit = daily_withdraw_limit
        self.fee = fee

    @property
    def overdraft_limit(self):
        return self._overdraft_limit

    @overdraft_limit.setter
    def overdraft_limit(self, value):
        if not str(value).strip():
            raise ValueError('overdraft_limit should be not null')
        if value < 0:
            raise ValueError("overdraft_limit can't be negative")
        self._overdraft_limit = value

    @property
    def daily_withdraw_limit(self):
        return self._daily_withdraw_limit

    @daily_withdraw_limit.setter
    def daily_withdraw_limit(self, value):
        if not str(value).strip():
            raise ValueError('daily_withdraw_limit should be not null')
        if value < 0:
            raise ValueError("daily_withdraw_limit can't be negative")
        self._daily_withdraw_limit = value

    @property
    def fee(self):
        return self._fee

    @fee.setter
    def fee(self, value):
        if not str(value).strip():
            raise ValueError('fee should be not null')
        if value < 0 or value > 1:
            raise ValueError("fee have to be between 0 and 1")
        self._fee = value

    def deposit(self, amount):
        super().deposit(amount)
        # Проверяем, был ли до этого долг
        if self.overdraft_limit != self.overdraft_balance:
            self.overdraft_balance += amount
            # Проверяем, закрыли ли долг
            if self.overdraft_balance > self.overdraft_limit:
                self.secure_balance = self.overdraft_balance - self.overdraft_limit
                self.overdraft_balance = self.overdraft_limit
                return f'Долг закрыт. Средства ({amount} {self.currency}) успешно внесены на счет. \n'
            else:
                self.secure_balance = 0
                return f'Средства ({amount} {self.currency}) успешно внесены в уплату долга. \n'
        else:
            return f'Средства ({amount} {self.currency}) успешно внесены на счет. \n'

    def withdraw(self, amount):
        if type(amount) is not int:
            raise InvalidOperationError(amount)
        current_balance = self.secure_balance - amount
        # После снятия долга не образовалось
        if current_balance >= 0:
            self.secure_balance = current_balance
        else:
            # До этой операции долга не было
            if self.overdraft_balance == self.overdraft_limit:
                # Процент считается на ту сумму, которая занимается из лимита
                curr_fee = abs(current_balance) * self.fee
            # До этой операции долг уже был
            else:
                # Процент начисляется на всю снимаемую сумму (т.к. она вся идет в заем)
                curr_fee = amount * self.fee
            # Добавляем процент к снимаемой сумме
            current_balance -= curr_fee
            # Проверка лимита заемных средств
            if abs(current_balance) <= self.overdraft_balance:
                self.overdraft_balance += current_balance
                self.secure_balance = 0
                return f'Средства ({amount} {self.currency}) успешно списаны со счета\n' \
                       f'с учетом комиссии ({curr_fee} {self.currency})\n'
            else:
                raise ValueError(
                    f'Превышен лимит снятия денег: {amount} {self.currency} (комиссия: {curr_fee} {self.currency}). \n')
        return f'Средства ({amount} {self.currency}) успешно списаны со счета\n'

    def get_account_info(self):
        super().get_account_info()
        return f'Уникальный идентификатор счёта: {self.Id}. \n' \
               f'Данные владельца: {self.person}. \n' \
               f'Защищённый баланс: {self.secure_balance}. \n' \
               f'Статус счёта: {self.status}. \n' \
               f'Лимит овердрафта: {self.overdraft_limit}. \n' \
               f'Осталось заемных средств: {self.overdraft_balance}. \n' \
               f'Лимит овердрафта на день (пока не используется): {self.daily_withdraw_limit}. \n' \
               f'Процентная ставка по овердрафту: {self.fee}. \n'

    def __str__(self):
        super().__str__()
        return f'Тип счёта: BankAccount. \n' \
               f'Владелец: {self.person}. \n' \
               f'Номер счета: {self.id_num}. \n' \
               f'Статус счёта: {self.status}. \n' \
               f'Баланс счета: {self.secure_balance} {self.currency}. \n' \
               f'Лимит овердрафта: {self.overdraft_limit}. \n' \
               f'Осталось заемных средств: {self.overdraft_balance}. \n' \
               f'Процентная ставка по овердрафту: {self.fee}. \n'


# Брокерский счет. Есть валюта, есть бумаги.
# Бумаги представляют собой словарь: наименование и кол-во вложенных средств.
# Теперь у пользователя есть 4 действия: внести деньги на счет (в валюту), купить бумаги (из валюты в бумаги),
# продать бумаги (из бумаги в валюту), вывести деньги (из валюты)
# При создании брокерского счета автоматически открываются позиции на 'stocks', 'bonds' и 'etf'
class InvestmentAccount(BankAccount):
    def __init__(self, Id, person, secure_balance, status, currency, yearly_growth_rate):
        super().__init__(Id, person, secure_balance, status, currency)
        self.yearly_growth_rate = yearly_growth_rate
        self.current_balance = secure_balance
        self.invest_dict = dict(stocks=0, bonds=0, etf=0)

    @property
    def yearly_growth_rate(self):
        return self._yearly_growth_rate

    @yearly_growth_rate.setter
    def yearly_growth_rate(self, value):
        if not str(value).strip():
            raise ValueError('yearly_growth_rate should be not null')
        if value < 0 or value > 1:
            raise ValueError("yearly_growth_rate have to be between 0 and 1")
        self._yearly_growth_rate = value

    def deposit(self, amount):
        super().deposit(amount)
        self.current_balance += amount
        return f'Средства ({amount} {self.currency}) успешно внесены на счет\n'

    def deposit_securities(self, security, amount):
        if security in self.invest_dict:
            if amount > self.current_balance:
                raise ValueError(
                    f"Недостаточно средств на счете. Вы можете потратить не более {self.current_balance} {self.currency}.\n")
            self.current_balance -= amount
            self.invest_dict[security] += amount
        else:
            raise ValueError(f"Покупка данной бумаги недоступна. Доступные бумаги: {list(self.invest_dict.keys())}")
        return f'Средства ({amount} {self.currency}) на покупку {security} успешно потрачены\n'

    def withdraw(self, amount):
        super().withdraw(amount)
        if amount > self.current_balance:
            self.secure_balance += amount
            raise ValueError(
                f"Недостаточно средств на счете. Доступны средства для снятия: {self.current_balance} {self.currency}")
        self.current_balance -= amount
        return f'Средства ({amount} {self.currency}) успешно списаны со счета\n'

    def project_yearly_growth(self):
        for security in list(self.invest_dict.keys()):
            self.secure_balance += self.invest_dict[security] * self.yearly_growth_rate
            self.invest_dict[security] += self.invest_dict[security] * self.yearly_growth_rate
        return f'Стоимость портфеля выросла на {self.yearly_growth_rate * 100}% \n'

    def withdraw_securities(self, security, amount):
        if security in self.invest_dict:
            if amount > self.invest_dict[security]:
                self.current_balance += self.invest_dict[security]
                buffer = self.invest_dict[security]
                self.invest_dict[security] = 0
                return f"Максимальная сумма для продажи {security} ({buffer} {self.currency}). " \
                       f"Она была переведена на валютный счет. \n"
            else:
                self.invest_dict[security] -= amount
                self.current_balance += amount
        else:
            raise ValueError(f"Продажа данной бумаги недоступна. Доступные бумаги: {list(self.invest_dict.keys())}")
        return f'Средства ({amount} {self.currency}) c продажи {security} успешно переведены на валютный счет.\n'

    def get_account_info(self):
        super().get_account_info()
        return f'Уникальный идентификатор счёта: {self.Id}. \n' \
               f'Данные владельца: {self.person}. \n' \
               f'Защищённый баланс: {self.secure_balance}. \n' \
               f'Статус счёта: {self.status}. \n' \
               f'Баланс брокерского счета: {self.secure_balance} {self.currency}. \n' \
               f'Баланс валюты: {self.current_balance} {self.currency}. \n' \
               f'Состав инвестиционного портфеля: {self.invest_dict}. \n'

    def __str__(self):
        super().__str__()
        return f'Тип счёта: BankAccount. \n' \
               f'Владелец: {self.person}. \n' \
               f'Номер счета: {self.id_num}. \n' \
               f'Статус счёта: {self.status}. \n' \
               f'Баланс брокерского счета: {self.secure_balance} {self.currency}. \n' \
               f'Баланс валюты: {self.current_balance} {self.currency}. \n' \
               f'Состав инвестиционного портфеля: {self.invest_dict}. \n'


# == Тестирование == #

# # ======================= #
# # Создание SavingsAccount
# active_one = SavingsAccount('', 'Vova', 200000, 'активный', 'RUB', 0.02)
#
# # Операции с SavingsAccount
# print(active_one.__str__())
# print(active_one.deposit(20000))
# print(active_one.__str__())
# print(active_one.withdraw(50000))
# print(active_one.__str__())
# print(active_one.apply_monthly_interest())
# print(active_one.__str__())
# print(active_one.get_account_info())
# print(active_one.__str__())
# # ======================= #

# ======================= #
# Создание PremiumAccount
active_one = PremiumAccount('', 'Vova', 200000, 'активный', 'RUB', 100000, 20000, 0.02)

# Операции с PremiumAccount
print(active_one.__str__())
# Пополнение счета
print(active_one.deposit(20000))
print(active_one.__str__())
# Снятие со счета
print(active_one.withdraw(50000))
print(active_one.__str__())
# Снятие со счета в долг
print(active_one.withdraw(200000))
print(active_one.__str__())
# Снятие с погашением долга
print(active_one.deposit(50000))
print(active_one.__str__())
# # Снятие сверх лимита
# print(active_one.withdraw(200000))
# print(active_one.__str__())
# print(active_one.get_account_info())
# ======================= #

# # ======================= #
# # Создание InvestmentAccount
# active_one = InvestmentAccount('', 'Vova', 200000, 'активный', 'RUB', 0.1)
# print(active_one.__str__())
# # Операции с InvestmentAccount
# # пополнение счета
# print(active_one.deposit(20000))
# print(active_one.__str__())
# # покупка бумаг
# print(active_one.deposit_securities('stocks', 100000))
# print(active_one.deposit_securities('bonds', 10000))
# print(active_one.deposit_securities('etf', 40000))
# print(active_one.__str__())
# # продажа бумаг
# print(active_one.withdraw_securities('stocks', 10000))
# print(active_one.withdraw_securities('bonds', 20000))
# print(active_one.withdraw_securities('etf', 10000))
# print(active_one.__str__())
# # снятие со счета
# print(active_one.withdraw(50000))
# print(active_one.__str__())
# # Рост ценных бумаг
# print(active_one.project_yearly_growth())
# print(active_one.__str__())
# # Недостаточно средств
# # print(active_one.deposit_securities('stocks', 200000))
# # print(active_one.__str__())
# # Неправильные бумаги
# # print(active_one.deposit_securities('stocksss', 100000))
# # print(active_one.__str__())
# # Продажа несуществующей бумаги
# # print(active_one.withdraw_securities('etfqwe', 10000))
# # print(active_one.__str__())
# # Вывод недоступной суммы
# # print(active_one.withdraw(5000000))
# # print(active_one.__str__())