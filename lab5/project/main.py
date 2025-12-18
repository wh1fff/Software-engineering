from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import uuid

# SINGLETON
class DatabaseConnection:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection = None
        return cls._instance
    
    def connect(self):
        if not self._initialized:
            print("🔌 Инициализация БД...")
            self._connection = "sqlite:///company.db"
            self._initialized = True
        return self._connection

# BUILDER
class EmployeeBuilder:
    def __init__(self):
        self._data = {}
    
    def set_id(self, id: int) -> 'EmployeeBuilder':
        self._data['id'] = id; return self
    
    def set_name(self, name: str) -> 'EmployeeBuilder':
        self._data['name'] = name; return self
    
    def set_department(self, dept: str) -> 'EmployeeBuilder':
        self._data['department'] = dept; return self
    
    def set_base_salary(self, salary: float) -> 'EmployeeBuilder':
        self._data['base_salary'] = salary; return self
    
    def set_developer(self, skills: List[str], seniority: str) -> 'EmployeeBuilder':
        self._data['type'] = 'developer'; self._data['skills'] = skills
        self._data['seniority'] = seniority; return self
    
    def build(self) -> 'DecoratedEmployee':
        return DecoratedEmployee(EmployeeFactory.create_employee(**self._data))

# BASE CLASSES
class AbstractEmployee(ABC):
    @abstractmethod
    def calculate_salary(self) -> float: pass
    @abstractmethod
    def get_info(self) -> str: pass

class Employee(AbstractEmployee):
    def __init__(self, id: int, name: str, department: str, base_salary: float):
        self.id = id; self.name = name; self.department = department
        self._base_salary = base_salary; self.projects = []
    
    def calculate_salary(self) -> float: return self._base_salary
    def get_info(self) -> str: return f"{self.name} ({self.department})"

class EmployeeFactory:
    @staticmethod
    def create_employee(**kwargs) -> AbstractEmployee:
        emp_type = kwargs.get('type', 'employee')
        if emp_type == 'developer':
            return Developer(**kwargs)
        return Employee(
            kwargs['id'],
            kwargs['name'],
            kwargs['department'],
            kwargs['base_salary']
        )


class Developer(Employee):
    def __init__(self, id: int, name: str, department: str, base_salary: float, skills: List[str], seniority: str):
        super().__init__(id, name, department, base_salary)
        self.skills = skills; self.seniority = seniority

# DECORATOR
class EmployeeDecorator(AbstractEmployee):
    def __init__(self, employee: AbstractEmployee):
        self._employee = employee
    
    def get_info(self) -> str: return self._employee.get_info()
    def calculate_salary(self) -> float: return self._employee.calculate_salary()

class BonusDecorator(EmployeeDecorator):
    def __init__(self, employee: AbstractEmployee, bonus: float):
        super().__init__(employee); self._bonus = bonus
    
    def calculate_salary(self) -> float:
        return super().calculate_salary() + self._bonus

class TrainingDecorator(EmployeeDecorator):
    def __init__(self, employee: AbstractEmployee, training: str):
        super().__init__(employee); self._training = training
    
    def get_info(self) -> str:
        return f"{super().get_info()} | Training: {self._training}"

# STRATEGY
class BonusStrategy(ABC):
    @abstractmethod
    def calculate_bonus(self, employee: AbstractEmployee) -> float: pass

class PerformanceBonusStrategy(BonusStrategy):
    def calculate_bonus(self, employee: AbstractEmployee) -> float:
        return employee._base_salary * 0.15

class ProjectBonusStrategy(BonusStrategy):
    def calculate_bonus(self, employee: AbstractEmployee) -> float:
        return len(employee.projects) * 5000

class SalesBonusStrategy(BonusStrategy):
    def calculate_bonus(self, employee: AbstractEmployee) -> float:
        return employee._base_salary * 0.375  # 37.5% от продаж

# OBSERVER
class Observer(ABC):
    @abstractmethod
    def update(self, subject: AbstractEmployee, old_salary: float): pass

class Subject:
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer): self._observers.append(observer)
    def detach(self, observer: Observer): self._observers.remove(observer)
    def notify_salary_change(self, employee: AbstractEmployee, old_salary: float):
        for observer in self._observers: observer.update(employee, old_salary)

class HRObserver(Observer):
    def update(self, subject: AbstractEmployee, old_salary: float):
        print(f" HR: {subject.name} - зарплата изменена с {old_salary} до {subject.calculate_salary()}")

class AccountingObserver(Observer):
    def update(self, subject: AbstractEmployee, old_salary: float):
        print(f" Бухгалтерия: Пересчет налогов для {subject.name}")

class HRSystem(Subject): pass
