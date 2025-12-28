from abc import ABC, abstractmethod
from typing import Dict, Any


class AbstractEmployee(ABC):

    def __init__(self, id: int, name: str, department: str, base_salary: float):
        self.__id = id
        self.__name = name
        self.__department = department
        self.__base_salary = base_salary

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def department(self):
        return self.__department

    @property
    def base_salary(self):
        return self.__base_salary

    @id.setter
    def id(self, value):
        value = int(value)
        if value < 1:
            raise ValueError("число должно быть >0")
        self.__id = value

    @name.setter
    def name(self, value):
        value = str(value)
        if value == "":
            raise ValueError("имя не должно быть пустым")
        self.__name = value

    @department.setter
    def department(self, value):
        value = str(value)
        if value == "":
            raise ValueError("отдел не должен быть пустым")
        self.__department = value

    @base_salary.setter
    def base_salary(self, value):
        value = int(value)
        if value < 1:
            raise ValueError("число должно быть >0")
        self.__base_salary = value

    @abstractmethod
    def calculate_salary(self) -> float:
        pass

    @abstractmethod
    def get_info(self) -> str:
        pass


class Employee(AbstractEmployee):

    def calculate_salary(self) -> float:
        return self.base_salary

    def get_info(self) -> str:
        return (
            f"cотрудник id: {self.id}, имя: {self.name}, отдел: {self.department}, "
            f"базовая зарплата: {self.base_salary}, итоговая зарплата: {self.calculate_salary()}"
        )

class Manager(Employee):

    def __init__(
        self, id: int, name: str, department: str, base_salary: float, bonus: float
    ):
        super().__init__(id, name, department, base_salary)
        self.__bonus = bonus

    @property
    def bonus(self):
        return self.__bonus

    @bonus.setter
    def bonus(self, value):
        value = float(value)
        if value < 0:
            raise ValueError("Бонус не может быть >0")
        self.__bonus = value

    def calculate_salary(self) -> float:
        return self.base_salary + self.bonus

    def get_info(self) -> str:
        return (
            f"менеджер id: {self.id}, имя: {self.name}, отдел: {self.department}, "
            f"базовая зарплата: {self.base_salary}, бонус: {self.bonus}, "
            f"итоговая зарплата: {self.calculate_salary()}"
        )

class Developer(Employee):

    def __init__(
        self,
        id: int,
        name: str,
        department: str,
        base_salary: float,
        tech_stack: list[str],
        seniority_level: str,
    ):
        super().__init__(id, name, department, base_salary)
        self.__tech_stack = tech_stack
        self.__seniority_level = seniority_level

    @property
    def tech_stack(self):
        return self.__tech_stack.copy()

    @property
    def seniority_level(self):
        return self.__seniority_level

    @seniority_level.setter
    def seniority_level(self, value):
        allowed_levels = ["junior", "middle", "senior"]
        if value not in allowed_levels:
            raise ValueError(
                f'уровень должен быть один из: {", ".join(allowed_levels)}'
            )
        self.__seniority_level = value

    def add_skill(self, new_skill: str) -> None:
        self.__tech_stack.append(new_skill)

    def calculate_salary(self) -> float:
        multipliers = {"junior": 1.0, "middle": 1.5, "senior": 2.0}
        return self.base_salary * multipliers[self.seniority_level]

    def get_info(self) -> str:
        return (
            f"разработчик id: {self.id}, имя: {self.name}, отдел: {self.department}, "
            f"базовая зарплата: {self.base_salary}, уровень: {self.seniority_level}, "
            f'стек технологий: {", ".join(self.tech_stack)}, '
            f"итоговая зарплата: {self.calculate_salary()}"
        )


class Salesperson(Employee):
    def __init__(
        self,
        id: int,
        name: str,
        department: str,
        base_salary: float,
        commission_rate: float,
        sales_volume: float,
    ):
        super().__init__(id, name, department, base_salary)
        self.__commission_rate = commission_rate
        self.__sales_volume = sales_volume

    @property
    def commission_rate(self):
        return self.__commission_rate

    @property
    def sales_volume(self):
        return self.__sales_volume

    @commission_rate.setter
    def commission_rate(self, value):
        value = float(value)
        if not 0 <= value <= 1:
            raise ValueError("ставка комиссии должна быть между 0 и 1")
        self.__commission_rate = value

    @sales_volume.setter
    def sales_volume(self, value):
        value = float(value)
        if value < 0:
            raise ValueError("объем продаж не может быть >0")
        self.__sales_volume = value

    def update_sales(self, new_sales: float) -> None:
        if new_sales < 0:
            raise ValueError("нельзя добавить объем продаж >0")
        self.__sales_volume += new_sales

    def calculate_salary(self) -> float:
        return self.base_salary + (self.commission_rate * self.sales_volume)

    def get_info(self) -> str:
        return (
            f"продавец id: {self.id}, имя: {self.name}, отдел: {self.department}, "
            f"базовая зарплата: {self.base_salary}, ставка комиссии: {self.commission_rate}, "
            f"объем продаж: {self.sales_volume}, итоговая зарплата: {self.calculate_salary()}"
        )


class EmployeeFactory:

    @staticmethod
    def create_employee(emp_type: str, **kwargs) -> AbstractEmployee:
        if emp_type == "employee":
            return Employee(
                id=kwargs.get("id"),
                name=kwargs.get("name"),
                department=kwargs.get("department"),
                base_salary=kwargs.get("base_salary"),
            )
        elif emp_type == "manager":
            return Manager(
                id=kwargs.get("id"),
                name=kwargs.get("name"),
                department=kwargs.get("department"),
                base_salary=kwargs.get("base_salary"),
                bonus=kwargs.get("bonus"),
            )
        elif emp_type == "developer":
            return Developer(
                id=kwargs.get("id"),
                name=kwargs.get("name"),
                department=kwargs.get("department"),
                base_salary=kwargs.get("base_salary"),
                tech_stack=kwargs.get("tech_stack", []),
                seniority_level=kwargs.get("seniority_level"),
            )
        elif emp_type == "salesperson":
            return Salesperson(
                id=kwargs.get("id"),
                name=kwargs.get("name"),
                department=kwargs.get("department"),
                base_salary=kwargs.get("base_salary"),
                commission_rate=kwargs.get("commission_rate"),
                sales_volume=kwargs.get("sales_volume"),
            )
        else:
            raise ValueError(f"Неизвестный тип сотрудника: {emp_type}")


def main():
    print("создание сотрудников через конструктор processing...")

    employee = Employee(1, "Иван Иванов", "Бухгалтерия", 50000)
    manager = Manager(2, "Петр Петров", "Менеджмент", 70000, 20000)
    developer = Developer(
        3, "Алексей Сидоров", "IT", 60000, ["Python", "Django", "PostgreSQL"], "middle"
    )
    salesperson = Salesperson(4, "Анна Козлова", "Продажи", 40000, 0.1, 150000)

    print("\demo работы сеттеров:")
    employee.name = "Иван Николаев"
    manager.bonus = 25000
    developer.add_skill("Redis")
    salesperson.update_sales(50000)

    employees = [employee, manager, developer, salesperson]
    for emp in employees:
        print("\n" + "-" * 40)
        print(f"ЗП: {emp.calculate_salary()}")
        print(emp.get_info())

    print("создание сотрудников через фабрику processing...")

    factory_employee = EmployeeFactory.create_employee(
        "employee", id=5, name="Мария Смирнова", department="HR", base_salary=45000
    )

    factory_manager = EmployeeFactory.create_employee(
        "manager",
        id=6,
        name="Олег Кузнецов",
        department="Администрация",
        base_salary=80000,
        bonus=30000,
    )

    factory_developer = EmployeeFactory.create_employee(
        "developer",
        id=7,
        name="Елена Орлова",
        department="Разработка",
        base_salary=90000,
        tech_stack=["Java", "Spring", "Hibernate"],
        seniority_level="senior",
    )

    factory_salesperson = EmployeeFactory.create_employee(
        "salesperson",
        id=8,
        name="Дмитрий Волков",
        department="Маркетинг",
        base_salary=50000,
        commission_rate=0.15,
        sales_volume=200000,
    )

    # demo полиморфного поведения
    print("\demo полиморфного поведения processing...")
    factory_employees = [
        factory_employee,
        factory_manager,
        factory_developer,
        factory_salesperson,
    ]

    for emp in factory_employees:
        print("\n" + "-" * 40)
        print(emp.get_info())


    print("смешанный списог сотрудников processing...")

    all_employees = employees + factory_employees
    for i, emp in enumerate(all_employees, 1):
        print(f"\n{i}. {emp.get_info()}")

if __name__ == "__main__":
    main()