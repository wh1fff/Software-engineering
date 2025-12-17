from typing import List, Dict, Optional

class Department:
    def __init__(self, name: str, code: str):
        self.__name = name
        self.__code = code
        self.__employees: List[AbstractEmployee] = []

    def add_employee(self, employee: AbstractEmployee) -> None:
        self.__employees.append(employee)

    def remove_employee(self, employee_id: int) -> None:
        self.__employees = [emp for emp in self.__employees if emp.id != employee_id]

    def calculate_total_salary(self) -> float:
        return sum(emp.calculate_salary() for emp in self.__employees)

    def get_employee_count(self) -> Dict[str, int]:
        counts = {}
        for emp in self.__employees:
            cls_name = emp.__class__.__name__
            counts[cls_name] = counts.get(cls_name, 0) + 1
        return counts

    def __len__(self) -> int:
        return len(self.__employees)

    def __getitem__(self, key: int) -> AbstractEmployee:
        return self.__employees[key]

    def __contains__(self, employee: AbstractEmployee) -> bool:
        return employee in self.__employees

    def __iter__(self):
        return iter(self.__employees)
    
dept = Department("IT", "DEV")
dept.add_employee(manager)
dept.add_employee(developer)
print(dept.calculate_total_salary())
print(len(dept))
for emp in dept:
    print(emp.get_info())