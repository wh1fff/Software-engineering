class EmployeeBuilder:
    def __init__(self):
        self._data: dict = {}

    def set_id(self, id: int) -> "EmployeeBuilder":
        self._data["id"] = id
        return self

    def set_name(self, name: str) -> "EmployeeBuilder":
        self._data["name"] = name
        return self

    def set_department(self, department: str) -> "EmployeeBuilder":
        self._data["department"] = department
        return self

    def set_base_salary(self, base_salary: float) -> "EmployeeBuilder":
        self._data["base_salary"] = base_salary
        return self

    def as_developer(self, tech_stack: list[str], seniority: str) -> "EmployeeBuilder":
        self._data["emp_type"] = "developer"
        self._data["tech_stack"] = tech_stack
        self._data["seniority_level"] = seniority
        return self

    def build(self) -> "AbstractEmployee":
        emp_type = self._data.get("emp_type", "employee")
        return EmployeeFactory.create_employee(emp_type, **self._data)
