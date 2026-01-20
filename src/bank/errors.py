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