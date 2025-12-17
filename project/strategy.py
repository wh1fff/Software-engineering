class BonusStrategy(ABC):
    @abstractmethod
    def calculate_bonus(self, employee: AbstractEmployee) -> float:
        ...

class PerformanceBonusStrategy(BonusStrategy):
    def calculate_bonus(self, employee: AbstractEmployee) -> float:
        return employee.base_salary * 0.1

class ExperienceBonusStrategy(BonusStrategy):
    def calculate_bonus(self, employee: AbstractEmployee) -> float:
        return employee.base_salary * 0.05 * getattr(employee, "years_of_experience", 1)

class BonusCalculator:
    def __init__(self, strategy: BonusStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: BonusStrategy) -> None:
        self._strategy = strategy

    def calculate_total(self, employee: AbstractEmployee) -> float:
        return employee.calculate_salary() + self._strategy.calculate_bonus(employee)
