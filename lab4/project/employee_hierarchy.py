from abc import ABC, abstractmethod
from typing import List

class AbstractEmployee(ABC):
    @abstractmethod
    def calculate_salary(self) -> float:
        pass
    
    @abstractmethod
    def get_info(self) -> str:
        pass

class Employee(AbstractEmployee):
    def __init__(self, id: int, name: str, department: str, base_salary: float):
        self.__id = id
        self.__name = name
        self.__department = department
        self.__base_salary = base_salary

    def calculate_salary(self) -> float:
        return self.__base_salary

    def get_info(self) -> str:
        return f"{self.__str__()}, зарплата: {self.calculate_salary()}"

class Manager(Employee):
    def __init__(self, id: int, name: str, department: str, base_salary: float, bonus: float):
        super().__init__(id, name, department, base_salary)
        self.__bonus = bonus

    def calculate_salary(self) -> float:
        return super().calculate_salary() + self.__bonus

class Developer(Employee):
    def __init__(self, id: int, name: str, department: str, base_salary: float, 
                 tech_stack: List[str], seniority: str):
        super().__init__(id, name, department, base_salary)
        self.__tech_stack = tech_stack
        self.__seniority = seniority

    def calculate_salary(self) -> float:
        coeff = {"junior": 1.0, "middle": 1.5, "senior": 2.0}
        return super().calculate_salary() * coeff.get(self.__seniority, 1.0)

class EmployeeFactory:
    @staticmethod
    def create_employee(emp_type: str, **kwargs) -> AbstractEmployee:
        if emp_type == "manager":
            return Manager(**kwargs)
        elif emp_type == "developer":
            return Developer(**kwargs)
        elif emp_type == "employee":
            return Employee(**kwargs)
        raise ValueError(f"Неизвестный тип: {emp_type}")
    

manager = EmployeeFactory.create_employee("manager", id=2, name="Петр Петров", 
                                         department="Менеджмент", base_salary=70000, bonus=20000)
print(manager.calculate_salary())