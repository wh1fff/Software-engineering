from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional


# ===================== Часть 1. Инкапсуляция =====================

class Employee:
    """Базовый класс сотрудника с приватными полями и валидацией."""

    def __init__(self, id: int, name: str, department: str, base_salary: float):
        self.id = id
        self.name = name
        self.department = department
        self.base_salary = base_salary

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, value: int) -> None:
        value = int(value)
        if value <= 0:
            raise ValueError("ID должен быть положительным")
        self.__id = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        value = value.strip()
        if not value:
            raise ValueError("Имя не может быть пустым")
        self.__name = value

    @property
    def department(self) -> str:
        return self.__department

    @department.setter
    def department(self, value: str) -> None:
        value = value.strip()
        if not value:
            raise ValueError("Отдел не может быть пустым")
        self.__department = value

    @property
    def base_salary(self) -> float:
        return self.__base_salary

    @base_salary.setter
    def base_salary(self, value: float) -> None:
        value = float(value)
        if value <= 0:
            raise ValueError("Зарплата должна быть положительной")
        self.__base_salary = value

    def __str__(self) -> str:
        return (
            f"Сотрудник [id: {self.id}, имя: {self.name}, "
            f"отдел: {self.department}, базовая зарплата: {self.base_salary}]"
        )


# ================= Часть 2. Наследование и абстракция =================

class AbstractEmployee(ABC):
    """Абстрактный базовый класс сотрудника."""

    def __init__(self, id: int, name: str, department: str, base_salary: float):
        self._emp = Employee(id, name, department, base_salary)

    @property
    def id(self) -> int:
        return self._emp.id

    @property
    def name(self) -> str:
        return self._emp.name

    @property
    def department(self) -> str:
        return self._emp.department

    @property
    def base_salary(self) -> float:
        return self._emp.base_salary

    @base_salary.setter
    def base_salary(self, value: float) -> None:
        self._emp.base_salary = value

    @abstractmethod
    def calculate_salary(self) -> float:
        ...

    @abstractmethod
    def get_info(self) -> str:
        ...

    def __str__(self) -> str:
        return str(self._emp)


class BaseEmployee(AbstractEmployee):
    """Обычный сотрудник: итоговая зарплата = базовой."""

    def calculate_salary(self) -> float:
        return self.base_salary

    def get_info(self) -> str:
        return f"{self}, итоговая зарплата: {self.calculate_salary()}"


class Manager(AbstractEmployee):
    """Менеджер с бонусом."""

    def __init__(self, id: int, name: str, department: str,
                 base_salary: float, bonus: float):
        super().__init__(id, name, department, base_salary)
        self.bonus = float(bonus)

    def calculate_salary(self) -> float:
        return self.base_salary + self.bonus

    def get_info(self) -> str:
        return f"{self}, бонус: {self.bonus}, итоговая зарплата: {self.calculate_salary()}"


class Developer(AbstractEmployee):
    """Разработчик с уровнем и стеком технологий."""

    LEVEL_COEFF = {"junior": 1.0, "middle": 1.5, "senior": 2.0}

    def __init__(self, id: int, name: str, department: str,
                 base_salary: float, tech_stack: list[str],
                 seniority_level: str):
        super().__init__(id, name, department, base_salary)
        self.tech_stack = tech_stack
        self.seniority_level = seniority_level.lower()

    def calculate_salary(self) -> float:
        coeff = self.LEVEL_COEFF.get(self.seniority_level, 1.0)
        return self.base_salary * coeff

    def get_info(self) -> str:
        stack = ", ".join(self.tech_stack)
        return (
            f"{self}, уровень: {self.seniority_level}, "
            f"технологии: {stack}, итоговая зарплата: {self.calculate_salary()}"
        )

    def __iter__(self):
        """Итерация по стеку технологий."""
        return iter(self.tech_stack)


class Salesperson(AbstractEmployee):
    """Продавец: базовая + процент с продаж."""

    def __init__(self, id: int, name: str, department: str,
                 base_salary: float, commission_rate: float,
                 sales_volume: float):
        super().__init__(id, name, department, base_salary)
        self.commission_rate = float(commission_rate)
        self.sales_volume = float(sales_volume)

    def calculate_salary(self) -> float:
        return self.base_salary + self.sales_volume * self.commission_rate

    def get_info(self) -> str:
        return (
            f"{self}, комиссия: {self.commission_rate}, "
            f"продажи: {self.sales_volume}, итоговая: {self.calculate_salary()}"
        )


class EmployeeFactory:
    """Фабрика для создания сотрудников разных типов."""

    @staticmethod
    def create_employee(emp_type: str, **kwargs) -> AbstractEmployee:
        emp_type = emp_type.lower()
        if emp_type == "manager":
            return Manager(**kwargs)
        if emp_type == "developer":
            return Developer(**kwargs)
        if emp_type == "salesperson":
            return Salesperson(**kwargs)
        return BaseEmployee(**kwargs)


# ========== Часть 3. Полиморфизм, магические методы, Department ==========

class Department:
    """Отдел: хранит список сотрудников разных типов."""

    def __init__(self, name: str, code: str):
        self.name = name
        self.code = code
        self._employees: list[AbstractEmployee] = []

    def add_employee(self, employee: AbstractEmployee) -> None:
        self._employees.append(employee)

    def get_employees(self) -> list[AbstractEmployee]:
        return list(self._employees)

    def calculate_total_salary(self) -> float:
        return sum(e.calculate_salary() for e in self._employees)

    # немного магических методов для удобства
    def __len__(self) -> int:
        return len(self._employees)

    def __iter__(self):
        return iter(self._employees)

    def __getitem__(self, index: int) -> AbstractEmployee:
        return self._employees[index]


# ========== Часть 4. Композиция и агрегация: Project и Company ==========

class Project:
    """Проект: композиция — внутри список сотрудников."""

    VALID_STATUSES = {"planning", "active", "completed", "cancelled"}

    def __init__(self, project_id: int, name: str,
                 description: str, deadline: str,
                 status: str = "planning"):
        self.project_id = int(project_id)
        self.name = name
        self.description = description
        self.deadline = datetime.strptime(deadline, "%Y-%m-%d")
        if status not in self.VALID_STATUSES:
            raise ValueError("Некорректный статус проекта")
        self.status = status
        self._team: list[AbstractEmployee] = []

    def add_team_member(self, employee: AbstractEmployee) -> None:
        self._team.append(employee)

    def get_team(self) -> list[AbstractEmployee]:
        return list(self._team)

    def calculate_total_salary(self) -> float:
        return sum(e.calculate_salary() for e in self._team)


class Company:
    """Компания: агрегация отделов и проектов."""

    def __init__(self, name: str):
        self.name = name
        self._departments: list[Department] = []
        self._projects: list[Project] = []

    def add_department(self, department: Department) -> None:
        self._departments.append(department)

    def add_project(self, project: Project) -> None:
        self._projects.append(project)

    def get_all_employees(self) -> list[AbstractEmployee]:
        result: list[AbstractEmployee] = []
        for d in self._departments:
            result.extend(d.get_employees())
        return result

    def calculate_total_monthly_cost(self) -> float:
        return sum(e.calculate_salary() for e in self.get_all_employees())
