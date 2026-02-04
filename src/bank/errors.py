# Ошибка: нельзя снять или пополнить счет, у которого статус "замороженный"
class AccountFrozenError:
    def __init__(self, current_status):
        self.current_status = current_status

    def get_reason(self):
        current_reason = f"""Невозможно провести операцию. Статус счета: {self.current_status}"""
        return current_reason

    def __str__(self):
        return f'Невозможно провести операцию.' \
               f'Статус счета: {self.current_status}'


# Ошибка: нельзя снять или пополнить счет, у которого статус "закрытый"
# class AccountClosedError(Exception):
class AccountClosedError:
    def __init__(self, current_status):
        self.current_status = current_status

    def get_reason(self):
        current_reason = f"""Невозможно провести операцию. 
                            Статус счета: {self.current_status}"""
        return current_reason

    def __str__(self):
        return f'Невозможно провести операцию. ' \
               f'Статус счета: {self.current_status}'


# Ошибка недопустимости операции: когда не можем выполнить операции снятия и пополнения: неправильные типы данных
# class InvalidOperationError(Exception):
class InvalidOperationError:
    def __init__(self, amount):
        self.amount = amount

    def get_reason(self):
        current_reason = f"""Невозможно выполнить операцию: неправильный тип данных. 
                                Текущий тип данных у {self.amount}: {type(self.amount)}. '
                                Требуемый тип данных: {type(1)}. """
        return current_reason

    def __str__(self):
        return f'Невозможно выполнить операцию: неправильный тип данных. ' \
               f'Текущий тип данных у {self.amount}: {type(self.amount)}. ' \
               f'Требуемый тип данных: {type(1)}. '


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