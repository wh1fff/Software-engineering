class EmployeeDecorator(AbstractEmployee):
    def __init__(self, employee: AbstractEmployee):
        self._employee = employee

    def calculate_salary(self) -> float:
        return self._employee.calculate_salary()

    def get_info(self) -> str:
        return self._employee.get_info()

class BonusDecorator(EmployeeDecorator):
    def __init__(self, employee: AbstractEmployee, bonus_amount: float):
        super().__init__(employee)
        self._bonus_amount = bonus_amount

    def calculate_salary(self) -> float:
        return super().calculate_salary() + self._bonus_amount

class TrainingDecorator(EmployeeDecorator):
    def __init__(self, employee: AbstractEmployee, training: str):
        super().__init__(employee)
        self._training = training

    def get_info(self) -> str:
        base = super().get_info()
        return f"{base} | Training: {self._training}"
