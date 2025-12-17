class Observer(ABC):
    @abstractmethod
    def update(self, employee: AbstractEmployee, old_salary: float) -> None:
      
class Subject:
    def __init__(self):
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify_salary_change(self, employee: AbstractEmployee, old_salary: float) -> None:
        for obs in self._observers:
            obs.update(employee, old_salary)

class HRObserver(Observer):
    def update(self, employee: AbstractEmployee, old_salary: float) -> None:
        print(f"[HR] Зарплата {employee.name} изменена с {old_salary} на {employee.calculate_salary()}")

class AccountingObserver(Observer):
    def update(self, employee: AbstractEmployee, old_salary: float) -> None:
        print(f"[Accounting] Пересчёт налогов для {employee.name}")
