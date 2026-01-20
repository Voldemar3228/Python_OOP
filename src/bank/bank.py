import abc
import datetime
import random  # для генерации UUID
import string  # для генерации UUID
from datetime import datetime, time  # для проверки временных промежутков
from abc import ABC, abstractmethod  # Импортируем необходимые модули для создания абстрактного класса
from .errors import (
    AccountFrozenError
    , AccountClosedError
    , InvalidOperationError
    , InsufficientFundsError
)


class AbstractAccount(abc.ABC):

    def __init__(self, Id, person, secure_balance, status):
        self.Id = Id  # уникальный идентификатор счёта
        self.person = person  # данные владельца
        self.secure_balance = secure_balance  # защищённый баланс
        self._status = status  # статус счёта: активный, замороженный, закрытый

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
    SUSPICIOUS_SUM = 300000  # Проверка на подозрительные действия, сумма денег
    SUSPICIOUS_TIME_START = time(5, 0)  # Проверка на подозрительные действия, время начала (5 утра)
    SUSPICIOUS_TIME_END = time(6, 0)  # Проверка на подозрительные действия, время конца (6 утра)
    FORBIDDEN_TIME_START = time(0, 0)  # Запрет транзакций, время начала (00:00 полночь)
    FORBIDDEN_TIME_END = time(5, 0)  # Запрет транзакций, время конца (5 утра)

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
        if self._status in ['закрытый', 'Закрытый']:
            raise ValueError("Нельзя изменить статус 'закрытый'.")
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

    def validate_operation_for_premium(self, amount):
        if type(amount) is not int:
            raise InvalidOperationError(amount)
        if self.status not in self.STATUS:
            print(f'Статусы могут принимать следующие значения: {self.STATUS}')
            raise ValueError(f'Запрет выполнения операции')
        if self.status in ['замороженный', 'Замороженный']:
            raise AccountFrozenError(self.status)
        if self.status in ['закрытый', 'Закрытый']:
            raise AccountClosedError(self.status)

    # Проверка операции на подозрительные действия
    # Возвращаем True, если операция подозрительная, иначе - False
    def is_suspicious_actions(self, check_sum):
        check_time = datetime.now().time()
        # Проверка на слишком большую сумму
        if check_sum >= self.SUSPICIOUS_SUM:
            print(f"Используется подозрительная сумма >= {check_sum}.")
            return True
        # Проверка на необычное время
        #   Если период включает в себя полночь
        if self.SUSPICIOUS_TIME_START > self.SUSPICIOUS_TIME_END:
            if check_time >= self.SUSPICIOUS_TIME_START or check_time <= self.SUSPICIOUS_TIME_END:
                print(f"Операция проводится в подозрительное время ({check_time}) ", end='')
                print(f"c {self.SUSPICIOUS_TIME_START} до 00:00 или с 00:00 до {self.SUSPICIOUS_TIME_END}.")
                return True
        else:
            if self.SUSPICIOUS_TIME_START <= check_time <= self.SUSPICIOUS_TIME_END:
                print(f"Операция проводится в подозрительное время ({check_time}) ", end='')
                print(f"c {self.SUSPICIOUS_TIME_START} до {self.SUSPICIOUS_TIME_END}.")
                return True
        return False

        # Проверка на запрет операции
        # Возвращаем True, если запрещено, иначе - False

    def is_forbidden_actions(self):
        check_time = datetime.now().time()
        #   Если период включает в себя полночь
        if self.FORBIDDEN_TIME_START > self.FORBIDDEN_TIME_END:
            if check_time >= self.FORBIDDEN_TIME_START or check_time <= self.FORBIDDEN_TIME_END:
                print(f"Операция проводится в запрещенное время ({check_time}) ", end='')
                print(f"c {self.FORBIDDEN_TIME_START} до 00:00 или с 00:00 до {self.FORBIDDEN_TIME_END}.")
                return True
        else:
            if self.FORBIDDEN_TIME_START <= check_time <= self.FORBIDDEN_TIME_END:
                print(f"Операция проводится в запрещенное время ({check_time}) ", end='')
                print(f"c {self.FORBIDDEN_TIME_START} до {self.FORBIDDEN_TIME_END}.")
                return True
        return False

    def deposit(self, amount):
        if self.is_suspicious_actions(amount) | self.is_forbidden_actions():
            print(f"В целях безопасности счет {self.Id} заморожен. Обратитесь в Банк за разморозкой. \n")
            self.status = 'замороженный'
            return False  # операция не выполнилась, добавить флаг клиенту "Подозрительная активность"
        self.validate_operation(amount, 'deposit')
        self.secure_balance += amount
        # print(f"Средства ({amount} {self.currency}) успешно внесены на счет\n")
        return True  # операция выполнилась, "Подозрительной активности" у клиента нет

    def withdraw(self, amount):
        if self.is_suspicious_actions(amount) | self.is_forbidden_actions():
            print(f"В целях безопасности счет {self.Id} заморожен. Обратитесь в Банк за разморозкой. \n")
            self.status = 'замороженный'
            return False  # операция не выполнилась, добавить флаг клиенту "Подозрительная активность"
        self.validate_operation(amount, 'withdraw')
        self.secure_balance -= amount
        # print(f"Средства ({amount} {self.currency}) успешно списаны со счета\n")
        return True  # операция выполнилась, "Подозрительной активности" у клиента нет

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


# ==================================================================================================================== #

# ==================================================================================================================== #
# =====================================================  Day 2  ====================================================== #
# ==================================================================================================================== #

class SavingsAccount(BankAccount):
    def __init__(self, Id, person, secure_balance, status, currency, monthly_rate):
        super().__init__(Id, person, secure_balance, status, currency)
        self.monthly_rate = monthly_rate
        self.min_balance = secure_balance
        self.first_operation = False

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
        # super().deposit(amount)
        # return f'Средства ({amount} {self.currency}) успешно внесены на счет\n'
        if super().deposit(amount):
            # Если счет пополняется впервые, пересчитывается минимальный остаток
            if not self.first_operation:
                self.min_balance = self.secure_balance
                self.first_operation = True
            print(f'Средства ({amount} {self.currency}) успешно внесены на счет "{self.Id}".\n')
            return True  # операция выполнилась успешно
        # return super().deposit(amount)
        self.status = 'замороженный'
        return False  # операция не выполнилась, добавить клиенту флаг "Подозрительные действия

    def withdraw(self, amount):
        if super().withdraw(amount):
            self.min_balance = min(self.secure_balance, self.min_balance)
            # return f'Средства ({amount} {self.currency}) успешно списаны со счета\n'
            print(f'Средства ({amount} {self.currency}) успешно списаны со счета "{self.Id}".\n')
            return True  # операция выполнилась успешно
        # return super().withdraw(amount)
        self.status = 'замороженный'
        return False  # операция не выполнилась, добавить клиенту флаг "Подозрительные действия"

    def apply_monthly_interest(self):
        buf = self.min_balance * self.monthly_rate
        self.secure_balance += buf
        self.min_balance = self.secure_balance
        return f'Средства ({buf} {self.currency}) успешно зачислены на счет "{self.Id}".\n' \
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
        # super().deposit(amount)
        if super().deposit(amount):
            # Проверяем, был ли до этого долг
            if self.overdraft_limit != self.overdraft_balance:
                self.overdraft_balance += amount
                # Проверяем, закрыли ли долг
                if self.overdraft_balance > self.overdraft_limit:
                    self.secure_balance = self.overdraft_balance - self.overdraft_limit
                    self.overdraft_balance = self.overdraft_limit
                    # return f'Долг закрыт. Средства ({amount} {self.currency}) успешно внесены на счет. \n'
                    print(f'Долг закрыт. Средства ({amount} {self.currency}) успешно внесены на счет "{self.Id}". \n')
                    return True  # операция выполнилась успешно
                else:
                    self.secure_balance = 0
                    # return f'Средства ({amount} {self.currency}) успешно внесены в уплату долга. \n'
                    print(f'Средства ({amount} {self.currency}) успешно внесены в уплату долга. \n')
                    return True  # операция выполнилась успешно
            else:
                # return f'Средства ({amount} {self.currency}) успешно внесены на счет. \n'
                print(f'Средства ({amount} {self.currency}) успешно внесены на счет "{self.Id}". \n')
                return True  # операция выполнилась успешно
        self.status = 'замороженный'
        return False  # операция не выполнилась, добавить клиенту флаг "Подозрительные действия

    def withdraw(self, amount):
        # if type(amount) is not int:
        #     raise InvalidOperationError(amount)
        self.validate_operation_for_premium(amount)
        if not (self.is_suspicious_actions(amount) | self.is_forbidden_actions()):
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
                    # return f'Средства ({amount} {self.currency}) успешно списаны со счета\n' \
                    #     f'с учетом комиссии ({curr_fee} {self.currency})\n'
                    print(f'Средства ({amount} {self.currency}) успешно списаны со счета "{self.Id}" \n', end='')
                    print(f'с учетом комиссии ({curr_fee} {self.currency})\n')
                    return True  # операция выполнилась успешно
                else:
                    raise ValueError(
                        f'Превышен лимит снятия денег: {amount} {self.currency} (комиссия: {curr_fee} {self.currency}). \n')
            # return f'Средства ({amount} {self.currency}) успешно списаны со счета\n'
            print(f'Средства ({amount} {self.currency}) успешно списаны со счета "{self.Id}".\n')
            return True  # операция выполнилась успешно
        self.status = 'замороженный'
        return False  # операция не выполнилась, добавить клиенту флаг "Подозрительные действия

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
        if super().deposit(amount):
            self.current_balance += amount
            # return f'Средства ({amount} {self.currency}) успешно внесены на счет\n'
            print(f'Средства ({amount} {self.currency}) успешно внесены на счет "{self.Id}".\n')
            return True  # операция выполнилась успешно
        self.status = 'замороженный'
        return False  # операция не выполнилась, добавить клиенту флаг "Подозрительные действия

    def deposit_securities(self, security, amount):
        if not (self.is_suspicious_actions(amount) | self.is_forbidden_actions()):
            if security in self.invest_dict:
                if amount > self.current_balance:
                    raise ValueError(
                        f'Недостаточно средств на счете "{self.Id}". Вы можете потратить не более {self.current_balance} {self.currency}.\n')
                self.current_balance -= amount
                self.invest_dict[security] += amount
            else:
                raise ValueError(f"Покупка данной бумаги недоступна. Доступные бумаги: {list(self.invest_dict.keys())}")
            # return f'Средства ({amount} {self.currency}) на покупку {security} успешно потрачены\n'
            print(f'Средства ({amount} {self.currency}) на покупку {security} успешно потрачены\n')
            return True  # операция выполнилась успешно
        self.status = 'замороженный'
        return False  # операция не выполнилась, добавить клиенту флаг "Подозрительные действия

    def withdraw(self, amount):
        if super().withdraw(amount):
            if amount > self.current_balance:
                self.secure_balance += amount
                raise ValueError(
                    f"Недостаточно средств на счете. Доступны средства для снятия: {self.current_balance} {self.currency}")
            self.current_balance -= amount
            # return f'Средства ({amount} {self.currency}) успешно списаны со счета\n'
            print(f'Средства ({amount} {self.currency}) успешно списаны со счета "{self.Id}".\n')
            return True  # операция выполнилась успешно
        self.status = 'замороженный'
        return False  # операция не выполнилась, добавить клиенту флаг "Подозрительные действия

    def project_yearly_growth(self):
        for security in list(self.invest_dict.keys()):
            self.secure_balance += self.invest_dict[security] * self.yearly_growth_rate
            self.invest_dict[security] += self.invest_dict[security] * self.yearly_growth_rate
        return f'Стоимость портфеля выросла на {self.yearly_growth_rate * 100}% \n'

    def withdraw_securities(self, security, amount):
        if not (self.is_suspicious_actions(amount) | self.is_forbidden_actions()):
            if security in self.invest_dict:
                if amount > self.invest_dict[security]:
                    self.current_balance += self.invest_dict[security]
                    buffer = self.invest_dict[security]
                    self.invest_dict[security] = 0
                    # return f"Максимальная сумма для продажи {security} ({buffer} {self.currency}). " \
                    #     f"Она была переведена на валютный счет. \n"
                    print(f'Максимальная сумма для продажи {security} ({buffer} {self.currency}). ', end='')
                    print(f'Она была переведена на валютный счет. \n')
                    return True  # операция выполнилась успешно
                else:
                    self.invest_dict[security] -= amount
                    self.current_balance += amount
            else:
                raise ValueError(f"Продажа данной бумаги недоступна. Доступные бумаги: {list(self.invest_dict.keys())}")
            # return f'Средства ({amount} {self.currency}) c продажи {security} успешно переведены на валютный счет.\n'
            print(f'Средства ({amount} {self.currency}) c продажи {security} успешно переведены на валютный счет.\n')
            return True  # операция выполнилась успешно
        self.status = 'замороженный'
        return False  # операция не выполнилась, добавить клиенту флаг "Подозрительные действия

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


# ==================================================================================================================== #
# =====================================================  Day 3  ====================================================== #
# ==================================================================================================================== #

class Bank:
    # Список констант, которые удобно менять в одном месте, а не искать по всему коду
    CLIENT_DB = []  # список клиентов (экземпляров класса Client)
    ACCOUNT_DB = []  # список счетов всех клиентов
    AUTH_TRIES = 3
    CURR_CLIENT = ''  # текущий клиент, нужен для авторизации
    ACCOUNT_TYPE = {'SavingsAccount': SavingsAccount
        , 'PremiumAccount': PremiumAccount
        , 'InvestmentAccount': InvestmentAccount}
    OVERDRAFT_TOTAL = 100000
    OVERDRAFT_DAILY = 25000
    PERCENT_RATE = 0.05

    def __init__(self, name):
        self.name = name

    # Метод добавления клиента
    # Атрибут add_client_id нужен для клиента его в системе Банка
    def add_client(self, add_full_name, add_client_id, add_contact_info, add_birthday, add_password):
        flag = False
        add_client_status = 'активный'
        # add_password = input('Введите пароль для текущего клиента: ')
        new_client = Client(add_full_name, add_client_id, add_client_status,
                            add_contact_info, add_birthday)
        # Проверка уникальности ID нового клиента
        while not flag:
            for search_client in self.CLIENT_DB:
                # если нашли совпадение по ID клиента
                if new_client.client_id == search_client.client.client_id:
                    print(f"Номер клиента занят. Ему будет присвоен другой номер \n")
                    add_client_id = ''  # При инициализации ID клиента будет рандомно сгенерирован
                    new_client = Client(add_full_name, add_client_id, add_client_status, add_contact_info, add_birthday)
                    break  # Начинаем новую итерацию проверки
            else:
                flag = True  # Проверка прошла успешно
        # Теперь можно добавлять клиента в базу Банка
        new_client_card = Bank_Client_card(new_client, add_password, [], False)
        self.CLIENT_DB.append(new_client_card)  # добавление клиента в базу Банка
        self.CURR_CLIENT = new_client_card  # добавленный клиент становится активным для совершения транзакций
        return f"""Клиент "{' '.join((new_client.full_name.values()))}" успешно добавлен в систему банка "{self.name}". \n"""

    # Создание счета: SavingAccounts, PremiumAccount или InvestmentAccount
    # Атрибут add_acc_id нужен для счета в системе Банка
    def open_account(self, add_account: str, add_acc_id, linked_person_id, add_currency):
        account = None
        # Проверка на создаваемый тип счета
        if add_account not in self.ACCOUNT_TYPE.keys():
            raise ValueError(f"Доступные для создания типы счетов: {self.ACCOUNT_TYPE.keys()} \n")
        # Проверка на существование клиента в системе банка
        for search_client in self.CLIENT_DB:
            if linked_person_id == search_client.client.client_id:
                full_name = ' '.join(list(search_client.client.full_name.values()))
                break
        else:
            raise ValueError(f"Клиент с номером {linked_person_id} не найден в банковской системе \n")
        flag = False  # для проверки уникальности ID счета
        if add_account == 'PremiumAccount':
            account = self.ACCOUNT_TYPE[add_account](add_acc_id, full_name, 0, 'активный', add_currency,
                                                     self.OVERDRAFT_TOTAL,
                                                     self.OVERDRAFT_DAILY, self.PERCENT_RATE)
            while not flag:
                for check_acc in self.ACCOUNT_DB:
                    # если нашли совпадение по ID счета
                    if check_acc.Id == account.Id:
                        # пересоздаем счет с новым ID
                        account = self.ACCOUNT_TYPE[add_account]('', full_name, 0, 'активный', add_currency,
                                                                 self.OVERDRAFT_TOTAL, self.OVERDRAFT_DAILY,
                                                                 self.PERCENT_RATE)
                        break  # Начинаем новую итерацию проверки
                else:
                    flag = True  # Проверка прошла успешно, можно добавлять счет в базу данных счетов Банка
        elif add_account in ['SavingsAccount', 'InvestmentAccount']:
            account = self.ACCOUNT_TYPE[add_account](add_acc_id, full_name, 0, 'активный', add_currency,
                                                     self.PERCENT_RATE)
            while not flag:
                for check_acc in self.ACCOUNT_DB:
                    if check_acc.Id == account.Id:
                        account = self.ACCOUNT_TYPE[add_account]('', full_name, 0, 'активный',
                                                                 add_currency, self.PERCENT_RATE)
                        break
                else:
                    flag = True  # Проверка прошла успешно, можно добавлять счет в базу данных счетов Банка

        # Добавление счета в карточку клиента
        for search_client in self.CLIENT_DB:
            if linked_person_id == search_client.client.client_id:
                search_client.accounts.append(account)
                break
        # Добавление в банковскую систему счетов
        self.ACCOUNT_DB.append(account)
        # Вывод информации об успешном создании счета
        print(f'Счет под номером "{add_acc_id}" успешно создан! \n')

    # Закрытие счета (без возможности поменять статус, навсегда)
    def close_account(self, close_id):
        for search_acc in self.ACCOUNT_DB:
            if search_acc.Id == close_id:
                search_acc.status = 'закрытый'
                print(f"""Статус счета "{close_id}" успешно изменен на "закрытый". \n""")
                # print(search_acc.__str__())  # можно вывести данные аккаунта и проверить измененный статус
                break
        else:
            print(f"Номер счета не найден! \n")

    # Заморозка счета
    def freeze_account(self, freeze_id):
        for search_acc in self.ACCOUNT_DB:
            if search_acc.Id == freeze_id:
                search_acc.status = 'замороженный'
                for search_client in self.CLIENT_DB:
                    for acc in search_client.accounts:
                        if freeze_id == acc.Id:
                            acc.status = 'замороженный'
                            break
                    else:
                        continue
                    break
                print(f"""Статус счета "{search_acc.Id}" успешно изменен на "замороженный". \n""")
                # print(search_acc.__str__())  # можно вывести данные аккаунта и проверить измененный статус
                break
        else:
            print(f"Номер счета не найден! \n")

    # Разморозка счета
    def unfreeze_account(self, frozen_id):
        for search_acc in self.ACCOUNT_DB:
            if search_acc.Id == frozen_id:
                if search_acc.status == 'замороженный':
                    search_acc.status = 'активный'
                    for search_client in self.CLIENT_DB:
                        for acc in search_client.accounts:
                            if frozen_id == acc.Id:
                                acc.status = 'активный'
                                break
                        else:
                            continue
                        break
                    print(f"""Статус счета {search_acc.Id} успешно изменен на "активный". \n""")
                else:
                    print(f"""Статус счета {search_acc.Id} не заморожен. \n""")
                # print(search_acc.__str__())  # можно вывести данные аккаунта и проверить измененный статус
                break
        else:
            print(f"Номер счета не найден! \n")
        pass

    # Закрытие клиента (без возможности поменять статус, навсегда)
    def close_client(self, close_id):
        for search_client in self.CLIENT_DB:
            if search_client.client.client_id == close_id:
                search_client.client.client_status = 'закрытый'
                print(f"""Статус клиента "{close_id}" успешно изменен на "закрытый". \n""")
                # print(search_client.client.__str__())  # можно вывести данные аккаунта и проверить измененный статус
                break
        else:
            print(f"Номер счета не найден! \n")

    # Заморозка клиента
    def freeze_client(self, freeze_id):
        for search_client in self.CLIENT_DB:
            if search_client.client.client_id == freeze_id:
                search_client.client.client_status = 'замороженный'
                print(f"""Статус счета "{freeze_id}" успешно изменен на "замороженный". \n""")
                # print(search_client.client.__str__())  # можно вывести данные аккаунта и проверить измененный статус
                break
        else:
            print(f"Номер счета не найден! \n")

    # Разморозка клиента
    def unfreeze_client(self, frozen_id):
        for search_client in self.CLIENT_DB:
            if search_client.client.client_id == frozen_id:
                if search_client.client.client_status in ['замороженный', 'Замороженный']:
                    search_client.client.client_status = 'активный'
                    print(f"""Статус клиента {frozen_id} успешно изменен на "активный". \n""")
                else:
                    print(f"""Статус счета {frozen_id} не заморожен. \n""")
                self.CURR_CLIENT = search_client
                # print(search_client.client.__str__())  # можно вывести данные аккаунта и проверить измененный статус
                break
        else:
            print(f"Номер счета не найден! \n")

    # Аутентификация клиента (3 попытки)
    def authenticate_client(self, name, entered_pswrd:str = None):
        if not entered_pswrd:
            entered_pswrd = ''
        # Поиск клиента в системе банка
        for search_client in self.CLIENT_DB:
            if search_client.client.client_id == name:
                # Проверка статуса клиента
                if search_client.client.client_status not in ['активный', 'Активный']:
                    print(f'Клиент "{name}" имеет статус "{search_client.client.client_status}". ', end='')
                    print(f'Обратитесь в банк за консультацией.')
                    return False
                # Получаем пароль для проверки
                pswrd = search_client.client_password
                if str(entered_pswrd) == str(pswrd):
                    print(f"Авторизация прошла успешно! \n")
                    self.CURR_CLIENT = search_client
                    self.AUTH_TRIES = 3
                    return True
                else:
                    self.AUTH_TRIES -= 1
                    if self.AUTH_TRIES == 0:
                        search_client.client.client_status = 'замороженный'
                        print(f"Попытки кончились. Клиент заморожен.")
                    print(f"Авторизация не прошла! \n")
                    return False

    # Поиск счета по Id
    def search_accounts(self, account_id):
        for acc in self.ACCOUNT_DB:
            if str(acc.Id) == str(account_id):
                print(acc.__str__())
                break
        else:
            print(f'Счета по номером "{account_id}" не существует. \n')
        pass

    # для удобства вывода всех клиентов и проверки их статусов
    def show_all_clients(self):
        for show_client in self.CLIENT_DB:
            print(show_client.client.__str__())
            print(f'Наличие подозрительных операций: {show_client.susp_act_flg} \n')

    # расчет баланса, используется в get_total_balance и get_clients_ranking
    def get_balance(self, client_id):
        summa = None
        for search_client in self.CLIENT_DB:
            if search_client.client.client_id == client_id:
                summa = 0
                for acc in search_client.accounts:
                    summa += acc.secure_balance
                return summa
        else:
            print(f'Клиента с номером "{client_id}" не существует. \n')
            # return False
            return summa

    # Получение баланса банка или конкретного клиента
    def get_total_balance(self, client_id:str = None):
        summa = 0
        if not client_id:
            for acc in self.ACCOUNT_DB:
                summa += acc.secure_balance
            print(f'Баланс банка равен {summa}. \n')
            # return True
            return summa
        else:
            buf = self.get_balance(client_id)
            if buf is not None:
                print(f'Баланс клиента "{client_id}" равен {buf}. \n')
                return buf
        return None

    # Вывод всех клиентов и баланса их счета от богатых к бедным
    def get_clients_ranking(self):
        # Сортируем словарь по балансу
        clients_ranking = dict()
        # Проходимся по всем клиентам и заполняем словарь
        for search_client in self.CLIENT_DB:
            balance = self.get_balance(search_client.client.client_id)
            clients_ranking[search_client] = balance
        # Сортируем словарь по убыванию
        sorted_dict = dict(sorted(clients_ranking.items(), key=lambda item: item[1], reverse=True))
        i = 1
        print(f'Список клиентов по балансу на счете.')
        for key, value in sorted_dict.items():
            full_name = ' '.join(list(key.client.full_name.values()))
            print(f'{i}) {full_name}, баланс: {value}.')
            i += 1
        return True

    # Проверка клиента на подозрительную операцию
    def is_suspicious_action(self, check_action):
        if not check_action():
            self.CURR_CLIENT.susp_act_flg = True

    def transaction(self, *args):
        # Распаковка атрибутов
        acc_Id, method, *others = args
        # Проверка, есть ли счет у текущего клиента
        for acc in self.CURR_CLIENT.accounts:
            if acc.Id == acc_Id:
                if self.CURR_CLIENT.client.client_status in ['закрытый', 'Закрытый']:
                    print(f'Статус клиента {self.CURR_CLIENT.client.client_status}, транзакция невозможна')
                    return False
                break
        # если нет, то ищем нужного клиента в базе и присваиваем ему статус "текущий"
        else:
            for search_client in self.CLIENT_DB:
                for search_acc in search_client.accounts:
                    if search_acc.Id == acc_Id:
                        if self.authenticate_client(search_client.client.client_id):
                            break
                        else:
                            print(f'Транзакция не прошла. \n')
                            return False
        for acc in self.CURR_CLIENT.accounts:
            if acc.Id == acc_Id:
                # Логика транзакции
                # получаем название метода
                cur_method = getattr(acc, method, None)
                # Проверка на существование метода
                if callable(cur_method):
                    # Проверка на тип счета, потому что передаем разные аргументы
                    if acc.__class__.__name__ in ['SavingsAccount', 'PremiumAccount']:
                        if method in ['deposit', 'withdraw']:
                            summa = others[0]
                            if not cur_method(summa):
                                self.CURR_CLIENT.susp_act_flg = True
                        else:
                            print(cur_method())
                        return True
                    if acc.__class__.__name__ == 'InvestmentAccount':
                        if method in ['deposit', 'withdraw']:
                            summa = others[0]
                            if not cur_method(summa):
                                self.CURR_CLIENT.susp_act_flg = True
                        elif method in ['deposit_securities', 'withdraw_securities']:
                            security = others[0]
                            summa = others[1]
                            if not cur_method(security, summa):
                                self.CURR_CLIENT.susp_act_flg = True
                        else:
                            print(cur_method())
                        return True
                else:
                    print("Метод не найден")
                    return False
            else:
                continue
        return False

    def __str__(self):
        print(f'Тип: Bank.')
        print(f'Наименование: {self.name}.')
        print(
            f'Текущий клиент: {' '.join(list(self.CURR_CLIENT.client.full_name.values()))} c номером "{self.CURR_CLIENT.client.client_id}"')
        print(f'Список клиентов: ')
        buf1 = 1
        for search_client in self.CLIENT_DB:
            full_name = ' '.join(list(search_client.client.full_name.values()))
            print(f'{buf1}) {full_name} c номером "{search_client.client.client_id}" имеет следующие счета: ')
            if not search_client.accounts:
                print(f'    Клиент не создал ни одного счета.')
            else:
                for i in range(len(search_client.accounts)):
                    print(f'    {i + 1}. {search_client.accounts[i].Id}')
        else:
            print('\n')


class Client:
    RANDOM_CLIENT_ID_LEN = 8

    def __init__(self, full_name, client_id, client_status, contact_info, birthday):
        self.full_name = dict(Фамилия=full_name.split(' ')[0], Имя=full_name.split(' ')[1],
                              Отчество=full_name.split(' ')[2])
        self.client_id = client_id
        self.client_status = client_status
        self.contact_info = dict(Телефон=contact_info.split(' ')[0], Почта=contact_info.split(' ')[1])
        self.birthday = birthday

    # Валидация входных параметров
    @property
    def full_name(self):
        return self._full_name

    @full_name.setter
    def full_name(self, value):
        if not value:
            raise ValueError('Full name have to be not null')
        self._full_name = value

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, value):
        if not value.strip():
            all_symbols = string.ascii_lowercase + string.digits  # все буквы английского алфавита в нижнем регистре + цифры
            value = ''.join(random.choice(all_symbols) for _ in range(self.RANDOM_CLIENT_ID_LEN))
        self._client_id = value

    @property
    def client_status(self):
        return self._client_status

    @client_status.setter
    def client_status(self, value):
        if not value.strip():
            raise ValueError('status should be not null')
        self._client_status = value

    @property
    def contact_info(self):
        return self._contact_info

    @contact_info.setter
    def contact_info(self, value):
        if not value:
            raise ValueError('Full name have to be not null')
        if '@' in value['Телефон']:
            raise ValueError(f"Enter phone number first and email second. \n")
        self._contact_info = value

    @property
    def birthday(self):
        return self._birthday

    @birthday.setter
    def birthday(self, value):
        if not value.strip():
            raise ValueError('birthday should be not null')
        self._birthday = value

    def __str__(self):
        return f'Тип: Client. \n' \
               f'Клиент: {self.full_name}. \n' \
               f'Номер клиента: {self.client_id}. \n' \
               f'Статус клиента: {self.client_status}. \n' \
               f'Контакты: {self.contact_info}. \n' \
               f'Дата рождения: {self.birthday}. \n'


class Bank_Client_card:
    def __init__(self, client: Client, client_password, accounts, susp_act_flg: bool = False):
        self.client = client
        self.client_password = client_password
        self.accounts = accounts
        self.susp_act_flg = susp_act_flg

    def __str__(self):
        pass
