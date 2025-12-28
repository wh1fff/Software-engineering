import pytest
from source_code import Employee


class TestEmployeeBasics:

    def test_employee_creation_valid(self):
        emp = Employee(1, "Alice", "IT", 5000)
        
        assert emp.id == 1
        assert emp.name == "Alice"
        assert emp.department == "IT"
        assert emp.base_salary == 5000
    
    def test_employee_str_representation(self):

        emp = Employee(1, "Alice", "IT", 5000)
        result = str(emp)
        assert "Alice" in result
        assert "IT" in result
        assert "5000" in result


class TestEmployeeValidation:
    
    def test_employee_id_validation_negative(self):
        with pytest.raises(ValueError, match="положительным"):
            Employee(-1, "Alice", "IT", 5000)
    
    def test_employee_id_validation_zero(self):
        with pytest.raises(ValueError, match="положительным"):
            Employee(0, "Alice", "IT", 5000)
    
    def test_employee_salary_validation_negative(self):
        with pytest.raises(ValueError, match="положительным"):
            Employee(1, "Alice", "IT", -5000)
    
    def test_employee_name_validation_empty(self):
        with pytest.raises(ValueError, match="не должна быть пустой"):
            Employee(1, "", "IT", 5000)
    
    def test_employee_department_validation_empty(self):
        with pytest.raises(ValueError, match="не должна быть пустой"):
            Employee(1, "Alice", "", 5000)


class TestEmployeeSette:
    
    def test_employee_setter_id(self):
        emp = Employee(1, "Alice", "IT", 5000)
        emp.id = 2
        assert emp.id == 2
    
    def test_employee_setter_id_invalid(self):
        emp = Employee(1, "Alice", "IT", 5000)
        with pytest.raises(ValueError):
            emp.id = -5
    
    def test_employee_setter_salary(self):
        emp = Employee(1, "Alice", "IT", 5000)
        emp.base_salary = 6000
        assert emp.base_salary == 6000
    
    def test_employee_setter_name(self):
        emp = Employee(1, "Alice", "IT", 5000)
        emp.name = "Bob"
        assert emp.name == "Bob"
    
    def test_employee_setter_department(self):
        emp = Employee(1, "Alice", "IT", 5000)
        emp.department = "HR"
        assert emp.department == "HR"


class TestEmployeeMethods:
    
    def test_employee_calculate_salary(self):
        emp = Employee(1, "Alice", "IT", 5000)
        salary = emp.calculate_salary()
        assert salary == 5000
    
    def test_employee_get_info(self):
        emp = Employee(1, "Alice", "IT", 5000)
        info = emp.get_info()
        assert "Alice" in info
        assert "5000" in info


class TestEmployeeParametrized:
    
    @pytest.mark.parametrize("emp_id,name,dept,salary", [
        (1, "Alice", "IT", 5000),
        (2, "Bob", "HR", 4500),
        (3, "Charlie", "Finance", 6000),
        (100, "Test User", "Support", 3500),
    ])
    def test_employee_creation_parametrized(self, emp_id, name, dept, salary):
        emp = Employee(emp_id, name, dept, salary)
        assert emp.id == emp_id
        assert emp.name == name
        assert emp.department == dept
        assert emp.base_salary == salary