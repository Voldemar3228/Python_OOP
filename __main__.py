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
        for i in range(-len(self.Id),0,1):
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


# == Тестирование == #

active_one = BankAccount('', 'Vova', 200000, 'активный', 'RUB')
freeze_one = BankAccount('', 'Ivan', 10000, 'Замороженный', 'USD')

# print(freeze_one.deposit(2000))  # Пополнение замороженного счета
# print(freeze_one.withdraw(2000))  # Снятие с замороженного счета

# print(active_one.get_account_info()) # Было
# print(active_one.deposit(20000))  # Пополнение активного счета
# print(active_one.__str__()) # Стало

print(active_one.get_account_info()) # Было
print(active_one.withdraw(20000))  # Снятие с активного счета
print(active_one.__str__()) # Стало