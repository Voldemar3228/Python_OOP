import abc
import datetime
import random  # для генерации UUID
import string  # для генерации UUID
from datetime import datetime, time  # для проверки временных промежутков
from abc import ABC, abstractmethod  # Импортируем необходимые модули для создания абстрактного класса


# ==================================================================================================================== #
# =====================================================  Day 1  ====================================================== #
# ==================================================================================================================== #
# Ошибка: нельзя снять или пополнить счет, у которого статус "замороженный"
class AccountFrozenError:
    def __init__(self, current_status):
        self.current_status = current_status

    def get_reason(self):
        current_reason = f"""Невозможно провести операцию.\n
                            Статус счета: {self.current_status}"""
        return current_reason

    def __str__(self):
        return f'Невозможно провести операцию.\n' \
               f'Статус счета: {self.current_status}'


# Ошибка: нельзя снять или пополнить счет, у которого статус "закрытый"
# class AccountClosedError(Exception):
class AccountClosedError:
    def __init__(self, current_status):
        self.current_status = current_status

    def get_reason(self):
        current_reason = f"""Невозможно провести операцию.\n
                            Статус счета: {self.current_status}"""
        return current_reason

    def __str__(self):
        return f'Невозможно провести операцию.\n' \
               f'Статус счета: {self.current_status}'


# Ошибка недопустимости операции: когда не можем выполнить операции снятия и пополнения: неправильные типы данных
# class InvalidOperationError(Exception):
class InvalidOperationError:
    def __init__(self, amount):
        self.amount = amount

    def get_reason(self):
        current_reason = f"""Невозможно выполнить операцию: неправильный тип данных.\n
                                Текущий тип данных у {self.amount}: {type(self.amount)}.\n'
                                Требуемый тип данных: {type(1)}.\n"""
        return current_reason

    def __str__(self):
        return f'Невозможно выполнить операцию: неправильный тип данных.\n' \
               f'Текущий тип данных у {self.amount}: {type(self.amount)}.\n' \
               f'Требуемый тип данных: {type(1)}.\n'


# Ошибка недостаточности средств - если хотим снять больше того, что есть на счете
# class InsufficientFundsError(Exception):
class InsufficientFundsError:
    def __init__(self, withdraw_sum, balance, curr):
        self.withdraw_sum = withdraw_sum
        self.balance = balance
        self.curr = curr

    def get_reason(self):
        current_reason = f"""Недопустимое значение. 
                            Вы не можете снять {self.withdraw_sum} {self.curr}, 
                            так как сумма больше, чем есть сейчас на счету ({self.balance} {self.curr})."""
        return current_reason

    def __str__(self):
        return f'Недопустимое значение.' \
               f'Вы не можете снять {self.withdraw_sum} {self.curr}, ' \
               f'так как сумма больше, чем есть сейчас на счету ({self.balance} {self.curr}).'


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
        # if value < 0:
        #     raise ValueError("secure_balance can't be negative")
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

    # Успех - True, провал - False + причина в reason
    def validate_operation(self, amount=None, oper_type=None, acc=None):
        if type(amount) is not int:
            error = InvalidOperationError(amount)
            reason = error.get_reason()
            return False, reason
        if self.status not in self.STATUS:
            reason = f"""Запрет выполнения операции. Статусы могут принимать следующие значения: {self.STATUS}"""
            return False, reason
        if self.status in ['замороженный', 'Замороженный']:
            error = AccountFrozenError(self.status)
            reason = error.get_reason()
            return False, reason
        if self.status in ['закрытый', 'Закрытый']:
            error = AccountClosedError(self.status)
            reason = error.get_reason()
            return False, reason
        # если у нас не премиальный клиент, проверяем отрицательный баланс
        if acc != 'premium':
            if oper_type == 'withdraw' and amount > self.secure_balance:
                error = InsufficientFundsError(amount, self.secure_balance, self.currency)
                reason = error.get_reason()
                return False, reason
        flg, msg = self.is_suspicious_actions(amount)
        # Проверка на подозрительные действия
        if flg is True:
            reason = f"Подозрительная активность. \n" + str(msg) + f"""В целях безопасности счет {self.Id} заморожен. 
                        Обратитесь в Банк за разморозкой. """  # \n
            self.status = 'замороженный'
            return False, reason  # операция не выполнилась, добавить флаг клиенту "Подозрительная активность"
        # Проверка на запрещенные действия
        flg, msg = self.is_forbidden_actions()
        if flg is True:
            reason = f"Подозрительная активность. \n" + str(msg) + f"""В целях безопасности счет {self.Id} заморожен. 
                                    Обратитесь в Банк за разморозкой. """  # \n
            self.status = 'замороженный'
            return False, reason  # операция не выполнилась, добавить флаг клиенту "Подозрительная активность"
        return True, None

    # Проверка операции на подозрительные действия
    # Возвращаем True, если операция подозрительная, иначе - False
    def is_suspicious_actions(self, check_sum):
        check_time = datetime.now().time()
        # Проверка на слишком большую сумму
        if check_sum >= self.SUSPICIOUS_SUM:
            reason = f"Используется подозрительная сумма >= {check_sum}."
            return True, reason
        # Проверка на необычное время
        #   Если период включает в себя полночь
        if self.SUSPICIOUS_TIME_START > self.SUSPICIOUS_TIME_END:
            if check_time >= self.SUSPICIOUS_TIME_START or check_time <= self.SUSPICIOUS_TIME_END:
                reason = f"""Операция проводится в подозрительное время ({check_time}) 
                            c {self.SUSPICIOUS_TIME_START} до 00:00 или с 00:00 до {self.SUSPICIOUS_TIME_END}."""
                return True, reason
        else:
            if self.SUSPICIOUS_TIME_START <= check_time <= self.SUSPICIOUS_TIME_END:
                reason = f"""Операция проводится в подозрительное время ({check_time}) 
                            c {self.SUSPICIOUS_TIME_START} до {self.SUSPICIOUS_TIME_END}."""
                return True, reason
        return False, None

    # Проверка на запрет операции
    # Возвращаем True, если запрещено, иначе - False
    def is_forbidden_actions(self):
        check_time = datetime.now().time()
        #   Если период включает в себя полночь
        if self.FORBIDDEN_TIME_START > self.FORBIDDEN_TIME_END:
            if check_time >= self.FORBIDDEN_TIME_START or check_time <= self.FORBIDDEN_TIME_END:
                reason = f"""Операция проводится в запрещенное время ({check_time})  
                            c {self.FORBIDDEN_TIME_START} до 00:00 или с 00:00 до {self.FORBIDDEN_TIME_END}."""
                return True, reason
        else:
            if self.FORBIDDEN_TIME_START <= check_time <= self.FORBIDDEN_TIME_END:
                print(f"Операция проводится в запрещенное время ({check_time}) ", end='')
                print(f"c {self.FORBIDDEN_TIME_START} до {self.FORBIDDEN_TIME_END}.")
                reason = f"""Операция проводится в запрещенное время ({check_time})   
                            c {self.FORBIDDEN_TIME_START} до {self.FORBIDDEN_TIME_END}."""
                return True, reason
        return False, None

    def deposit(self, amount):
        # ============= new version =============
        # Проверка перед выполнением операции
        val_flg, val_msg = self.validate_operation(amount, 'deposit')
        if val_flg is False:
            return False, val_msg
        else:
            # операция выполнилась, "Подозрительной активности" у клиента нет
            self.secure_balance += amount
            # val_msg = f"Средства ({amount} {self.currency}) успешно внесены на счет\n"
        return val_flg, val_msg

    def withdraw(self, amount, acc=None):
        # ============= new version =============
        val_flg, val_msg = self.validate_operation(amount, 'withdraw', acc)
        if val_flg is False:
            return False, val_msg
        else:
            # операция выполнилась, "Подозрительной активности" у клиента нет
            self.secure_balance -= amount
        return val_flg, val_msg

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
        # check_msg = f'Подозрительная активность.'
        flg, msg = super().deposit(amount)
        if flg is True:
            # Если счет пополняется впервые, пересчитывается минимальный остаток
            if not self.first_operation:
                self.min_balance = self.secure_balance
                self.first_operation = True
            msg = f'Средства ({amount} {self.currency}) успешно внесены на счет "{self.Id}".'  # \n
        return flg, msg

    def withdraw(self, amount):
        check_msg = f'Подозрительная активность.'
        flg, msg = super().withdraw(amount)
        # if super().withdraw(amount):
        if flg is True:
            self.min_balance = min(self.secure_balance, self.min_balance)
            msg = f'Средства ({amount} {self.currency}) успешно списаны со счета "{self.Id}".'  # \n
            # return True, msg  # операция выполнилась успешно
        # else:
        #     self.status = 'замороженный'  # операция не выполнилась, добавить клиенту флаг "Подозрительные действия"
        return flg, msg

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
        return f'Тип счёта: SavingsAccount. \n' \
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
        check_msg = f'Подозрительная активность.'
        flg, msg = super().deposit(amount)
        # if super().deposit(amount):
        if flg is True:
            # Проверяем, был ли до этого долг
            if self.overdraft_limit != self.overdraft_balance:
                self.overdraft_balance += amount
                # Проверяем, закрыли ли долг
                if self.overdraft_balance > self.overdraft_limit:
                    self.secure_balance = self.overdraft_balance - self.overdraft_limit
                    self.overdraft_balance = self.overdraft_limit
                    msg = f'Долг закрыт. Средства ({amount} {self.currency}) успешно внесены на счет. '  # \n
                    # print(f'Долг закрыт. Средства ({amount} {self.currency}) успешно внесены на счет "{self.Id}". \n')
                    # return True, msg  # операция выполнилась успешно
                else:
                    self.secure_balance = 0
                    msg = f'Средства ({amount} {self.currency}) успешно внесены в уплату долга. '  # \n
                    # print(f'Средства ({amount} {self.currency}) успешно внесены в уплату долга. \n')
                    # return True, msg  # операция выполнилась успешно
            else:
                msg = f'Средства ({amount} {self.currency}) успешно внесены на счет. '  # \n
                # print(f'Средства ({amount} {self.currency}) успешно внесены на счет "{self.Id}". \n')
                # return True, msg  # операция выполнилась успешно
        # else:
        #     self.status = 'замороженный'  # операция не выполнилась, добавить клиенту флаг "Подозрительные действия
        return flg, msg

    def withdraw(self, amount):
        check_msg = f'Подозрительная активность.'
        flg, msg = super().withdraw(amount, 'premium')
        if flg is True:
            current_balance = self.secure_balance
            # После снятия долга не образовалось
            if current_balance >= 0:
                self.secure_balance = current_balance
                msg = f'Средства ({amount} {self.currency}) успешно списаны со счета'  # \n
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
                    msg = f"""Средства ({amount} {self.currency}) успешно списаны со счета\n'  
                           с учетом комиссии ({curr_fee} {self.currency})"""  # \n
                else:
                    msg = f"""Превышен лимит снятия денег: {amount} {self.currency} 
                            (комиссия: {curr_fee} {self.currency}). """  # \n
                    flg = False
        return flg, msg

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
        return f'Тип счёта: PremiumAccount. \n' \
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
        flg, msg = super().deposit(amount)
        if flg is True:
            self.current_balance += amount
            msg = f'Средства ({amount} {self.currency}) успешно внесены на счет "{self.Id}"'  # \n
        return flg, msg

    def deposit_securities(self, security, amount):
        flg, msg = self.validate_operation(amount, oper_type='deposit_securities')
        if flg is True:
            if security in self.invest_dict:
                if amount > self.current_balance:
                    msg = f"""Недостаточно средств на счете "{self.Id}".
                     Вы можете потратить не более {self.current_balance} {self.currency}."""  # \n
                    flg = False
                else:
                    self.current_balance -= amount
                    self.invest_dict[security] += amount
                    msg = f'Средства ({amount} {self.currency}) на покупку {security} успешно потрачены'  # \n
            else:
                msg = f"Покупка данной бумаги недоступна. Доступные бумаги: {list(self.invest_dict.keys())}"
                flg = False
        return flg, msg

    def withdraw(self, amount):
        flg, msg = super().withdraw(amount)
        if flg is True:
            if amount > self.current_balance:
                msg = f"Недостаточно средств на счете. Доступны средства для снятия: {self.current_balance} {self.currency}"
                flg = False
            else:
                self.current_balance -= amount
                msg = f'Средства ({amount} {self.currency}) успешно списаны со счета "{self.Id}".'  # \n
        return flg, msg

    def project_yearly_growth(self):
        for security in list(self.invest_dict.keys()):
            self.secure_balance += self.invest_dict[security] * self.yearly_growth_rate
            self.invest_dict[security] += self.invest_dict[security] * self.yearly_growth_rate
        return f'Стоимость портфеля выросла на {self.yearly_growth_rate * 100}% '  # \n

    def withdraw_securities(self, security, amount):
        flg, msg = super().withdraw(amount, 'withdraw_securities')
        if flg is True:
            if security in self.invest_dict:
                if amount > self.invest_dict[security]:
                    self.current_balance += self.invest_dict[security]
                    buffer = self.invest_dict[security]
                    self.invest_dict[security] = 0
                    print(f'Максимальная сумма для продажи {security} ({buffer} {self.currency}). ', end='')
                    print(f'Она была переведена на валютный счет. ')  # \n
                    msg = f"""Максимальная сумма для продажи {security} ({buffer} {self.currency}). '
                            Она была переведена на валютный счет. """  # \n
                    return True, msg  # операция выполнилась успешно
                else:
                    self.invest_dict[security] -= amount
                    self.current_balance += amount
                    msg = f"""Средства ({amount} {self.currency}) c продажи {security} 
                            успешно переведены на валютный счет."""  # \n
            else:
                msg = f"Продажа данной бумаги недоступна. Доступные бумаги: {list(self.invest_dict.keys())}"
                flg = False
        return flg, msg

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
        return f'Тип счёта: InvestmentAccount. \n' \
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
        self.client_db = []  # список клиентов (экземпляров класса Client)
        self.account_db = []  # список счетов всех клиентов

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
            for search_client in self.client_db:
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
        self.client_db.append(new_client_card)  # добавление клиента в базу Банка
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
        for search_client in self.client_db:
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
                for check_acc in self.account_db:
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
                for check_acc in self.account_db:
                    if check_acc.Id == account.Id:
                        account = self.ACCOUNT_TYPE[add_account]('', full_name, 0, 'активный',
                                                                 add_currency, self.PERCENT_RATE)
                        break
                else:
                    flag = True  # Проверка прошла успешно, можно добавлять счет в базу данных счетов Банка

        # Добавление счета в карточку клиента
        for search_client in self.client_db:
            if linked_person_id == search_client.client.client_id:
                search_client.accounts.append(account)
                break
        # Добавление в банковскую систему счетов
        self.account_db.append(account)
        # Вывод информации об успешном создании счета
        print(f'Счет под номером "{add_acc_id}" успешно создан! \n')

    # Закрытие счета (без возможности поменять статус, навсегда)
    def close_account(self, close_id):
        for search_acc in self.account_db:
            if search_acc.Id == close_id:
                search_acc.status = 'закрытый'
                print(f"""Статус счета "{close_id}" успешно изменен на "закрытый". \n""")
                # print(search_acc.__str__())  # можно вывести данные аккаунта и проверить измененный статус
                break
        else:
            print(f"Номер счета не найден! \n")

    # Заморозка счета
    def freeze_account(self, freeze_id):
        for search_acc in self.account_db:
            if search_acc.Id == freeze_id:
                search_acc.status = 'замороженный'
                for search_client in self.client_db:
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
        for search_acc in self.account_db:
            if search_acc.Id == frozen_id:
                if search_acc.status == 'замороженный':
                    search_acc.status = 'активный'
                    for search_client in self.client_db:
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
        for search_client in self.client_db:
            if search_client.client.client_id == close_id:
                search_client.client.client_status = 'закрытый'
                print(f"""Статус клиента "{close_id}" успешно изменен на "закрытый". \n""")
                # print(search_client.client.__str__())  # можно вывести данные аккаунта и проверить измененный статус
                break
        else:
            print(f"Номер счета не найден! \n")

    # Заморозка клиента
    def freeze_client(self, freeze_id):
        # for search_client in self.CLIENT_DB:
        for search_client in self.client_db:
            if search_client.client.client_id == freeze_id:
                search_client.client.client_status = 'замороженный'
                print(f"""Статус счета "{freeze_id}" успешно изменен на "замороженный". \n""")
                # print(search_client.client.__str__())  # можно вывести данные аккаунта и проверить измененный статус
                break
        else:
            print(f"Номер счета не найден! \n")

    # Разморозка клиента
    def unfreeze_client(self, frozen_id):
        for search_client in self.client_db:
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
    def authenticate_client(self, name, entered_pswrd: str = None):
        if not entered_pswrd:
            entered_pswrd = ''
        # Поиск клиента в системе банка
        for search_client in self.client_db:
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
        for acc in self.account_db:
            if str(acc.Id) == str(account_id):
                print(acc.__str__())
                break
        else:
            print(f'Счета по номером "{account_id}" не существует. \n')
        pass

    # для удобства вывода всех клиентов и проверки их статусов
    def show_all_clients(self):
        for show_client in self.client_db:
            print(show_client.client.__str__())
            print(f'Наличие подозрительных операций: {show_client.susp_act_flg} \n')

    # расчет баланса, используется в get_total_balance и get_clients_ranking
    def get_balance(self, client_id):
        summa = None
        for search_client in self.client_db:
            if search_client.client.client_id == client_id:
                summa = 0
                for acc in search_client.accounts:
                    summa += acc.secure_balance
                return summa
        else:
            print(f'Клиента с номером "{client_id}" не существует. \n')
            return summa

    # Получение баланса банка или конкретного клиента
    def get_total_balance(self, client_id: str = None):
        summa = 0
        if not client_id:
            for acc in self.account_db:
                summa += acc.secure_balance
            print(f'Баланс банка равен {summa}. \n')
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
        for search_client in self.client_db:
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

    # поиск ID клиента по ID его счета (для 5 дня)
    def get_client_id(self, client_acc):
        for search_client in self.client_db:
            for acc in search_client.accounts:
                if acc.Id == client_acc:
                    return search_client.client.client_id
        else:
            return None

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
            for search_client in self.client_db:
                for search_acc in search_client.accounts:
                    if search_acc.Id == acc_Id:
                        if self.authenticate_client(search_client.client.client_id):
                            break
                        else:
                            print(f'Транзакция не прошла. \n')
                            return False
        for acc in self.CURR_CLIENT.accounts:
            check_msg = f'Подозрительная активность.'
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
                            flg, msg = cur_method(summa)
                            if flg is False:
                                self.CURR_CLIENT.susp_act_flg = True
                        else:
                            print(cur_method())
                        return True
                    if acc.__class__.__name__ == 'InvestmentAccount':
                        if method in ['deposit', 'withdraw']:
                            summa = others[0]
                            flg, msg = cur_method(summa)
                            if flg is False and check_msg in msg:
                                self.CURR_CLIENT.susp_act_flg = True
                        elif method in ['deposit_securities', 'withdraw_securities']:
                            security = others[0]
                            summa = others[1]
                            flg, msg = cur_method(security, summa)
                            if flg is False and check_msg in msg:
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
        # for search_client in self.CLIENT_DB:
        for search_client in self.client_db:
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


# ==================================================================================================================== #
# =====================================================  Day 5  ====================================================== #
# ==================================================================================================================== #

# Логи по каждой транзакции, инстансы будут храниться в аудите
class Log:
    # ID, priority, sender, receiver, Type, Sum, currency, timestamps, security
    def __init__(self, trans_id, sender_Bank, sender_client_id, sender_acc,
                 receiver_Bank, receiver_client_id, receiver_acc, Sum, currency,
                 timestamps, trans_status, trans_description):
        self.trans_id = trans_id  # ID транзакции
        if sender_acc is not None:
            self.sender_Bank = sender_Bank.name  # Банк отправителя
            self.sender_client_id = sender_client_id  # ID отправителя
            self.sender_acc = sender_acc  # ID счета отправителя
        else:
            self.sender_Bank = None
            self.sender_client_id = None
            self.sender_acc = None
        if receiver_acc is not None:
            self.receiver_Bank = receiver_Bank.name  # Банк получателя
            self.receiver_client_id = receiver_client_id  # ID получателя
            self.receiver_acc = receiver_acc  # ID счета получателя
        else:
            self.receiver_Bank = None
            self.receiver_client_id = None
            self.receiver_acc = None
        self.Sum = Sum  # Сумма транзакции
        self.currency = currency  # Валюта транзакции
        self.timestamps = timestamps  # Время начала выполнения транзакции
        self.trans_status = trans_status  # Результат выполнения транзакции
        self.description = trans_description  # Описание выполненной транзакции
        # self.severity = random.choice(['INFO', 'WARNING', 'ERROR'])
        self.severity = 'INFO'  # Уровень важности лога
        pass

    # Логика по определению важности лога
    def set_severity(self):
        pass

    def log_info(self):
        result = f"""{self.severity}, {self.trans_id}, {self.sender_Bank}, {self.sender_client_id}, {self.sender_acc}, \
{self.receiver_Bank}, {self.receiver_client_id}, {self.receiver_acc}, {self.Sum}, \
{self.currency}, {self.timestamps}, {self.trans_status},{self.description} \n"""
        return result

    def __str__(self):
        pass


# Можно подключить к процессору методом и пользоваться им
class AuditLog:
    SOURCE_CODE = ['level', 'type', 'tx_id', 'client_id']
    def __init__(self, file_name):
        # self.severity = severity  # уровень важности (INFO / WARNING / ERROR)
        self.file_name = file_name + '.txt'
        self.log_db = []
        with open(self.file_name, 'w', encoding='utf-8') as f:
            f.write('Структура логов:\n')
            f.write('Уровень важности, ID транзакции, Банк отправителя, ID отправителя, ID счета отправителя, \
            Банк получателя, ID получателя, ID счета получателя, Сумма транзакции, алюта транзакции, \
            Время начала выполнения транзакции, Результат выполнения транзакции, Описание выполненной транзакции\n')
            f.write('Перечень логов:\n')
        pass

    # Создание лога
    def apply_log(self, got_log: Log):
        self.write_to_memory(got_log)
        self.write_to_file(got_log)

    # Запись лога в память
    def write_to_memory(self, curr_log: Log):
        self.log_db.append(curr_log)
        pass

    # Запись лога в файл
    def write_to_file(self, curr_log: Log):
        with open(self.file_name, 'a', encoding='utf-8') as f:
            f.write(curr_log.log_info())
        pass

    # Фильтрация логов (по уровню, типу события, tx_id, client_id)
    def filtration(self, source):
        if source in self.SOURCE_CODE:
            pass
        else:
            print(f'Доступные команды: {self.SOURCE_CODE}')


    def __str__(self):
        pass


# Наверное стоит его подключить к процессору отдельным методом, работает во время обработки транзакции
class RiskAnalyzer:
    def __init__(self, risk_level):
        self.risk_level = risk_level  # низкий, средний, высокий
        pass

    # Проверка на крупную сумму
    def check_suspicious_sum(self, amount):
        pass

    # Проверка на частые операции
    def check_suspicious_freq_operation(self):
        pass

    # Проверка на переводы на новые счета
    def check_new_transfer(self):
        pass

    # Проверка на ночные операции
    def check_late_time(self):
        pass

    def __str__(self):
        pass


# ==================================================================================================================== #
# =====================================================   END   ====================================================== #
# ==================================================================================================================== #


# ==================================================================================================================== #
# =====================================================  Day 4  ====================================================== #
# ==================================================================================================================== #

# timestamps: если timestamps не передается, ему ставится текущее время
# timestamps: если время будет больше, когда транзакция должна начаться, то она будет отложена
class Transaction:
    PRIORITY_LIST = [1, 2, 3, 4, 5]  # от более значимых к менее значимым
    INITIAL_FEE = 0

    def __init__(self, ID, priority, sender, receiver, Type, Sum, currency, *args):
        self.ID = ID
        self.Type = Type
        self.Sum = Sum
        self.currency = currency
        self.fee = self.INITIAL_FEE
        self.sender = sender
        self.receiver = receiver
        self.status = None
        self.description = ''
        # self.priority_code = random.choice(self.PRIORITY_LIST)
        self.priority_code = priority
        self.security = None
        if args[1] is not None:
            self.timestamps = args[1]
            self.security = args[0]
        elif args[0] is not None:
            self.timestamps = args[0]
        else:
            self.timestamps = datetime.now()

    def __str__(self):
        pass


# Очередь, имеет уникальный ID и хранит в себе список транзакций на выполнение.
class TransactionQueue:
    def __init__(self, transactions: Transaction = None):
        self.transaction_list = list(transactions) if transactions is not None else []

    def __str__(self):
        pass

    def add_transaction(self, transaction: Transaction):
        # ставим статус "ожидание выполнения"
        transaction.status = 'PENDING'
        # добавляем транзакцию в список
        self.transaction_list.append(transaction)
        # сортируем список по приоритету
        self.transaction_list.sort(key=lambda obj: obj.priority_code)

    def cancel_transaction(self, transaction_id):
        for trans in self.transaction_list:
            if trans.status == 'PENDING' and trans.ID == transaction_id:
                trans.status = 'CANCELED'
                break


# хранит в себе очередь транзакций
# Хранит в себе результаты выполнения предыдущей очереди транзакций
# редактирует очередь
# запускает выполнение очереди
class TransactionProcessor:
    RANDOM_ID_LEN = 8
    RETRY_ATTEMPTS = 3
    AVAILABLE_STATUS = ['PENDING', 'SUCCESS', 'FAILED', 'CANCELED']
    PREVIOUS_RESULT = []
    EXTERNAL_FEE_SUM = 1
    EXTERNAL_FEE_CURRENCY = 'USD'

    def __init__(self):
        all_symbols = string.ascii_lowercase + string.digits  # все буквы английского алфавита в нижнем регистре + цифры
        Id = ''.join(random.choice(all_symbols) for _ in range(self.RANDOM_ID_LEN))
        self.processorId = Id
        self.current_queue = TransactionQueue()
        self.bank_list = []
        self.auditlog = None
        self.risk_analyser = None
        pass

    # Добавление банков в работу процессора
    def add_bank(self, bank: Bank):
        self.bank_list.append(bank)

    # Добавление AuditLog в работу процессора
    def add_AuditLog(self, audit: AuditLog):
        self.auditlog = audit

    # Добавление RiskAnalyzer в работу процессора
    def add_RiskAnalyzer(self, r_a: RiskAnalyzer):
        self.risk_analyser = r_a

    # Создание лога
    def make_log(self, curr_trans: Transaction):
        # Если счет отправителя не пустой
        if curr_trans.sender is not None:
            # Получение счета и Банка отправителя по ID счета отправителя
            get_sender_acc, get_sender_Bank = self.is_found_acc(curr_trans.sender)
            print(get_sender_acc.Id)
            get_sender_acc_id = get_sender_acc.Id
            # Получение ID клиента по ID счета отправителя
            get_sender_client_id = get_sender_Bank.get_client_id(curr_trans.sender)
        else:
            # get_sender_acc_id, get_sender_Bank, get_sender_client_id = None, None, None
            get_sender_acc_id = None
            get_sender_Bank = None
            get_sender_client_id = None
        # Если счет получателя не пустой
        if curr_trans.receiver is not None:
            # Получение счета и Банка отправителя по ID счета отправителя
            get_receiver_acc, get_receiver_Bank = self.is_found_acc(curr_trans.receiver)
            get_receiver_acc_id = get_receiver_acc.Id
            # Получение ID клиента по ID счета отправителя
            get_receiver_client_id = get_receiver_Bank.get_client_id(curr_trans.receiver)
        else:
            # get_receiver_acc_id, get_receiver_Bank, get_receiver_client_id = None, None, None
            get_receiver_acc_id = None
            get_receiver_Bank = None
            get_receiver_client_id = None
        # Создание лога
        current_log = Log(curr_trans.ID, get_sender_Bank, get_sender_client_id, get_sender_acc_id,
                          get_receiver_Bank, get_receiver_client_id, get_receiver_acc_id, curr_trans.Sum,
                          curr_trans.currency, curr_trans.timestamps, curr_trans.status, curr_trans.description)
        # Добавление лога в аудит
        if self.auditlog is not None:
            self.auditlog.apply_log(current_log)
        else:
            raise ValueError(f'Подключите AuditLog к транзакционному процессору!')

    def add_transaction_in_queue(self, queue_id, queue_sender, queue_receiver, queue_Type, queue_Sum, queue_currency,
                                 queue_security=None, queue_timestamps=None, queue_priority=None):
        # Правила распределения приоритета
        if queue_priority is None:
            queue_sender_acc, queue_sender_bank = self.is_found_acc(queue_sender)
            queue_receiver_acc, queue_receiver_bank = self.is_found_acc(queue_sender)
            if queue_sender_bank != queue_receiver_bank:
                queue_priority = 1
            elif queue_sender_acc is None or queue_receiver_acc is None:
                if queue_Type == 'deposit':
                    queue_priority = 2
                if queue_Type in ['deposit_securities', 'withdraw_securities']:
                    queue_priority = 3
                if queue_Type == 'withdraw':
                    queue_priority = 4
            elif queue_sender_acc is not None and queue_receiver_acc is not None:
                if queue_Type == 'deposit':
                    queue_priority = 2
                elif queue_Type == 'withdraw':
                    queue_priority = 3
            else:
                queue_priority = 5

        # Создание транзакции
        current_transaction = Transaction(queue_id
                                          , queue_priority
                                          , queue_sender
                                          , queue_receiver
                                          , queue_Type
                                          , queue_Sum
                                          , queue_currency
                                          , queue_security
                                          , queue_timestamps
                                          )
        self.current_queue.add_transaction(current_transaction)

    def set_transaction_to_cancel(self, queue_id):
        self.current_queue.cancel_transaction(queue_id)
        pass

    # # Считает комиссию
    # def calculate_fee(self):
    #     pass

    # Поиск счета в БД банка
    def is_found_acc(self, acc_id):
        # Поиск по банкам
        for bank in self.bank_list:
            # Поиск по счетам банка
            for acc in bank.account_db:
                if str(acc.Id) == str(acc_id):
                    return acc, bank
        return None, None

    #  RUB, USD, EUR, KZT, CNY
    def convert(self, cur_from, cur_to, summa):
        if cur_from == cur_to:
            return summa
        if cur_to == 'RUB':
            if cur_from == 'USD':
                return summa * 80
            if cur_from == 'EUR':
                return summa * 90
            if cur_from == 'KZT':
                return summa * 0.15
            if cur_from == 'CNY':
                return summa * 11
        if cur_to == 'USD':
            if cur_from == 'RUB':
                return summa * 0.013
            if cur_from == 'EUR':
                return summa * 1.17
            if cur_from == 'KZT':
                return summa * 0.002
            if cur_from == 'CNY':
                return summa * 0.14
        if cur_to == 'EUR':
            if cur_from == 'RUB':
                return summa * 0.011
            if cur_from == 'USD':
                return summa * 0.85
            if cur_from == 'KZT':
                return summa * 0.0017
            if cur_from == 'CNY':
                return summa * 0.12
        if cur_to == 'KZT':
            if cur_from == 'RUB':
                return summa * 6.64
            if cur_from == 'USD':
                return summa * 504.34
            if cur_from == 'EUR':
                return summa * 590.87
            if cur_from == 'CNY':
                return summa * 72.18
        if cur_to == 'CNY':
            if cur_from == 'RUB':
                return summa * 0.092
            if cur_from == 'USD':
                return summa * 6.97
            if cur_from == 'EUR':
                return summa * 8.19
            if cur_from == 'KZT':
                return summa * 0.014

    # Проверяет правила
    def check_rules(self, check_sender, check_receiver, check_Type, check_Sum, check_currency, check_security=None):
        # == проверяем наличие счетов == #
        flg = False
        msg = ''
        sender = None
        receiver = None
        # если оба счета пустые - ошибка
        if check_sender is None and check_receiver is None:
            msg = f'Cчета отправителя и получателя не могут быть пустыми одновременно.'
            # flg = False
            return flg, msg
        # если счет отправителя пустой
        elif check_sender is None:
            receiver, receiver_bank = self.is_found_acc(check_receiver)
            if receiver is None:
                msg = f'Cчет получателя не найден в банковской системе счетов.'
                # flg = False
                return flg, msg
            # Конвертация валюты
            if receiver.currency != check_currency:
                receiver_sum = self.convert(check_currency, receiver.currency, check_Sum)
            else:
                receiver_sum = check_Sum
            # Выбор операции
            if check_Type in [
                'deposit'
                , 'withdraw'
                , 'apply_monthly_interest'
                , 'deposit_securities'
                , 'withdraw_securities'
                , 'project_yearly_growth']:
                if check_Type == 'deposit':
                    flg, msg = receiver.deposit(receiver_sum)
                if check_Type == 'withdraw':
                    flg, msg = receiver.withdraw(receiver_sum)
                if check_Type == 'apply_monthly_interest':
                    flg, msg = receiver.apply_monthly_interest()
                if check_Type == 'deposit_securities' and check_security is not None:
                    flg, msg = receiver.deposit_securities(check_security, receiver_sum)
                if check_Type == 'withdraw_securities' and check_security is not None:
                    flg, msg = receiver.withdraw_securities(check_security, receiver_sum)
                if check_Type == 'project_yearly_growth':
                    flg, msg = receiver.project_yearly_growth(receiver_sum, check_security)
            else:
                msg = f'Тип операции неопознан. Некорректный метод "{check_Type}".'
            return flg, msg
        # если счет получателя пустой
        elif check_receiver is None:
            sender, sender_bank = self.is_found_acc(check_sender)
            if sender is None:
                # return f'Cчет отправителя не найден в банковской системе счетов.'
                msg = f'Cчет отправителя не найден в банковской системе счетов.'
                # flg = False
                return flg, msg
            # Конвертация валюты
            if sender.currency != check_currency:
                sender_sum = self.convert(check_currency, sender.currency, check_Sum)
            else:
                sender_sum = check_Sum
            # Выбор операции
            if check_Type in [
                'deposit'
                , 'withdraw'
                , 'apply_monthly_interest'
                , 'deposit_securities'
                , 'withdraw_securities'
                , 'project_yearly_growth']:
                if check_Type == 'deposit':
                    flg, msg = sender.deposit(sender_sum)
                if check_Type == 'withdraw':
                    flg, msg = sender.withdraw(sender_sum)
                if check_Type == 'apply_monthly_interest':
                    flg, msg = sender.apply_monthly_interest()
                if check_Type == 'deposit_securities' and check_security is not None:
                    flg, msg = sender.deposit_securities(check_security, sender_sum)
                if check_Type == 'withdraw_securities' and check_security is not None:
                    flg, msg = sender.withdraw_securities(check_security, sender_sum)
                if check_Type == 'project_yearly_growth':
                    flg, msg = sender.project_yearly_growth(sender_sum, check_security)
            else:
                msg = f'Тип операции неопознан. Некорректный метод "{check_Type}".'
            return flg, msg
        # если происходит транзакция между счетами
        else:
            sender, sender_bank = self.is_found_acc(check_sender)
            receiver, receiver_bank = self.is_found_acc(check_receiver)

            # Проверка на внешнюю операцию
            if sender_bank.name != receiver_bank.name:
                external_flg = True
            else:
                external_flg = False
            # == конвертация == #
            external_sum = self.EXTERNAL_FEE_SUM
            external_currency = self.EXTERNAL_FEE_CURRENCY
            # if sender is not None and sender.currency != check_currency:
            if sender.currency != check_currency:
                sender_sum = self.convert(check_currency, sender.currency, check_Sum)
            else:
                sender_sum = check_Sum
            # if receiver is not None and receiver.currency != check_currency:
            if receiver.currency != check_currency:
                receiver_sum = self.convert(check_currency, receiver.currency, check_Sum)
            else:
                receiver_sum = check_Sum

        # == Выбор операции == #
        if check_Type in ['deposit', 'withdraw']:
            if check_Type == 'deposit':
                sender_flg, sender_msg = sender.deposit(sender_sum)
                if external_flg is True:
                    if external_currency != receiver.currency:
                        external_sum = self.convert(external_currency, receiver.currency, external_sum)
                    receiver_flg, receiver_msg = receiver.withdraw(receiver_sum + external_sum)
                else:
                    receiver_flg, receiver_msg = receiver.withdraw(receiver_sum)
            elif check_Type == 'withdraw':
                if external_flg is True:
                    if external_currency != sender.currency:
                        external_sum = self.convert(external_currency, sender.currency, external_sum)
                    sender_flg, sender_msg = sender.withdraw(sender_sum + external_sum)
                else:
                    sender_flg, sender_msg = sender.withdraw(sender_sum)
                receiver_flg, receiver_msg = receiver.deposit(receiver_sum)

            # === Проверка статуса транзакции === #
            # Если транзакция прошла успешно
            if sender_flg and receiver_flg is True:
                msg = sender_msg + receiver_msg
                flg = True
            # Если транзакция прервалась, вывести статус и код ошибки
            else:
                # если проблема возникла на стороне отправителя и получателя
                if sender_flg is False and receiver_flg is False:
                    msg = sender_msg + receiver_msg
                    flg = False
                # проблема возникла на стороне отправителя, откат транзакции получателя
                elif sender_flg is False:
                    msg = sender_msg
                    flg = sender_flg
                    if check_Type == 'deposit':
                        if external_flg is True:
                            receiver.deposit(receiver_sum + external_sum)
                        else:
                            receiver.deposit(receiver_sum)
                    if check_Type == 'withdraw':
                        receiver.withdraw(receiver_sum)
                # проблема возникла на стороне получателя, откат транзакции отправителя
                elif receiver_flg is False:
                    msg = receiver_msg
                    flg = receiver_flg
                    if check_Type == 'deposit':
                        sender.withdraw(sender_sum)
                    if check_Type == 'withdraw':
                        if external_flg is True:
                            sender.deposit(sender_sum + external_sum)
                        else:
                            sender.deposit(sender_sum)
            # === =========================== === #
        else:
            msg = f'Некорректный метод "{check_Type}". Можно выбрать только "withdraw" или "deposit".'
        return flg, msg

    # Если время в будущем, возвращаем False, иначе - True
    def check_time(self, time):
        if type(time) == str:
            time = datetime.strptime(time, '%d.%m.%Y')
        if time > datetime.now():
            return False
        return True

    # Выполнение транзакции. будет вызывать check_rules и calculate_fee
    def apply_transaction(self):
        start_later_trans = []
        # начинаем перебирать отсортированный список транзакций
        for trans in self.current_queue.transaction_list:
            if trans.status == 'CANCELED':
                trans.description = f'Транзакция не выполнилась из-за ее статуса: {trans.status}.'
                self.PREVIOUS_RESULT.append(trans)
                self.make_log(trans)
            elif trans.status == 'PENDING':
                # self, ID, sender, receiver, Type, Sum, currency, timestamps = None
                # Проверка времени старта транзакции
                if not self.check_time(trans.timestamps):
                    start_later_trans.append(trans)
                    continue
                # Проверка правил осуществления транзакций
                flg, msg = self.check_rules(trans.sender, trans.receiver, trans.Type, trans.Sum, trans.currency,
                                            trans.security)
                if flg is False:
                    trans.status = 'FAILED'
                    trans.description = f'Транзакция прервана! ' + str(msg)
                    self.PREVIOUS_RESULT.append(trans)
                    self.make_log(trans)
                    continue
                trans.status = 'SUCCESS'
                trans.description = f'Транзакция выполнилась успешно. ' + str(msg)
                self.PREVIOUS_RESULT.append(trans)
                self.make_log(trans)
            else:
                trans.description = f"""Транзакция не выполнилась из-за ее неверного статуса: "{trans.status}".
                                    Статусы могут принимать значения: '{"', '".join(self.AVAILABLE_STATUS)}'"""
                self.PREVIOUS_RESULT.append(trans)
                self.make_log(trans)
        # начинаем перебирать список отложенных транзакций
        for trans in start_later_trans:
            flg, msg = self.check_rules(trans.sender, trans.receiver, trans.Type, trans.Sum, trans.currency,
                                        trans.security)
            if flg is False:
                trans.status = 'FAILED'
                trans.description = f'Транзакция прервана! ' + str(msg)
                self.PREVIOUS_RESULT.append(trans)
                self.make_log(trans)
                continue
            trans.status = 'SUCCESS'
            trans.description = f'Транзакция выполнилась успешно. ' + str(msg)
            self.PREVIOUS_RESULT.append(trans)
            self.make_log(trans)
        # Обнуляем очередь
        self.current_queue = TransactionQueue()

    # Выводит информацию пользователю
    def __str__(self):
        print(f"Номер транзакционного процессора : {self.processorId}")
        buf = 1
        print("Очередь состоит из следующих транзакций: ")
        for trans in self.current_queue.transaction_list:
            print(f'    {buf}) "{trans.ID}" со статусом "{trans.status}" и кодом приоритета "{trans.priority_code}" ')
            buf += 1
        if buf == 1:
            print("     Ни одной транзакции нет в очереди. \n")
        print("Результат транзакций в предыдущей очереди: ")
        buf = 1
        for trans in self.PREVIOUS_RESULT:
            print(f'    {buf}) "{trans.ID}" со статусом "{trans.status}" ({trans.description}) ')
            buf += 1
        if buf == 1:
            print("     Очередь еще ни разу не запускалась. \n")
        pass


# не забыть про отчеты

# ================================================================ #
# ========================= Тестирование ========================= #
# ================================================================ #
# Создание Банка
new_bank = Bank('Новый банк')
old_bank = Bank('Старый банк')
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
#
#
print(old_bank.add_client('Петров Петр Петрович', 'poiu', '738923 dj@jd.com', '12.03.2005', 444))
old_bank.open_account('SavingsAccount', 'mmm', 'poiu', 'RUB')





new_processor = TransactionProcessor()

audit_log = AuditLog('AuditLog2')
new_processor.add_AuditLog(audit_log)

new_processor.add_bank(new_bank)
new_processor.add_bank(old_bank)
# new_bank.search_accounts('qqq')
# new_bank.search_accounts('www')
new_bank.search_accounts('mmm')
old_bank.search_accounts('mmm')
# new_processor.add_transaction_in_queue('qwer', None, 'qqq',
#                                        'deposit', 1000, 'RUB', queue_priority=5)
new_processor.add_transaction_in_queue('qwer', None, 'qqq',
                                       'deposit', 1000, 'RUB')
# new_processor.add_transaction_in_queue('qwer2', 'qqq', 'www',
#                                        'withdraw', 1, 'USD', "20.12.2026")
# new_processor.add_transaction_in_queue('qwer3', 'ccc', None,
#                                        'deposit', 1, 'USD', "etf", "20.12.2026")
# new_processor.add_transaction_in_queue('qwer4', 'ccc', None,
#                                        'deposit_securities', 1, 'USD', "etf", "20.12.2026")
# new_processor.add_transaction_in_queue('asd', 'qqq', 'sss',
#                                        'deposit', 1000, 'RUB')
# new_processor.add_transaction_in_queue('zxcv', 'qqq', 'ccc',
#                                        'deposit', 1000, 'RUB')
new_processor.add_transaction_in_queue('qwer2', None, 'mmm',
                                       'deposit', 10000, 'RUB')
new_processor.add_transaction_in_queue('qwer3', 'qqq', 'mmm',
                                       'deposit', 2, 'USD')
# new_processor.add_transaction_in_queue('qwer2', None, 'mmm',
#                                        'deposit', 10000, 'RUB', queue_priority=4)
# new_processor.add_transaction_in_queue('qwer3', 'qqq', 'mmm',
#                                        'deposit', 2, 'USD', queue_priority=1)
# new_processor.set_transaction_to_cancel('zxcv')
new_processor.apply_transaction()
new_processor.__str__()

# new_bank.search_accounts('qqq')
# old_bank.search_accounts('mmm')
# new_bank.search_accounts('ccc')

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
