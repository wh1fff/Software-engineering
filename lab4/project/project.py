from typing import List
from datetime import datetime

class Project:
    VALID_STATUSES = ["planning", "active", "completed", "cancelled"]

    def __init__(self, project_id: int, name: str, description: str, 
                 deadline: str, status: str = "planning"):
        self.__project_id = project_id
        self.__name = name
        self.__description = description
        self.__deadline = datetime.strptime(deadline, "%Y-%m-%d")
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Неверный статус: {status}")
        self.__status = status
        self.__team: List[AbstractEmployee] = []

    @property
    def project_id(self):
        return self.__project_id

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        if value not in self.VALID_STATUSES:
            raise ValueError(f"Неверный статус: {value}")
        self.__status = value

    def add_team_member(self, employee: AbstractEmployee) -> None:
        self.__team.append(employee)

    def calculate_total_salary(self) -> float:
        return sum(emp.calculate_salary() for emp in self.__team)

class Company:
    def __init__(self, name: str):
        self.__name = name
        self.__departments: List[Department] = []
        self.__projects: List[Project] = []

    def add_department(self, dept: Department) -> None:
        self.__departments.append(dept)

    def add_project(self, project: Project) -> None:
        self.__projects.append(project)

    def calculate_total_monthly_cost(self) -> float:
        total = 0
        for dept in self.__departments:
            total += dept.calculate_total_salary()
        return total
    
project = Project(101, "AI Platform", "AI система", "2025-12-31", "active")
project.add_team_member(developer)
company = Company("TechInnovations")
company.add_project(project)
print(company.calculate_total_monthly_cost())