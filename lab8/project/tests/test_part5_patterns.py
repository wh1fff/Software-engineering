import pytest
from unittest.mock import Mock
from source_code import (
    Employee,
    Manager,
    Developer,
    DatabaseConnection,
    EmployeeBuilder,
    SalaryAdapter,
    BonusDecorator
)


class TestSingletonPattern:
    
    def test_singleton_database_connection(self):
        db1 = DatabaseConnection()
        db2 = DatabaseConnection()
        assert db1 is db2
        assert id(db1) == id(db2)
    
    def test_singleton_connection_state(self):
        db1 = DatabaseConnection()
        db2 = DatabaseConnection()
        assert db1 is db2


class TestBuilderPattern:
    
    def test_builder_pattern_employee(self):
        emp = (EmployeeBuilder()
              .set_id(1)
              .set_name("John")
              .set_department("IT")
              .set_base_salary(5000)
              .build())
        assert emp.id == 1
        assert emp.name == "John"
        assert emp.calculate_salary() == 5000
    
    def test_builder_pattern_developer(self):
        dev = (EmployeeBuilder()
              .set_id(1)
              .set_name("Alice")
              .set_department("DEV")
              .set_base_salary(5000)
              .set_type("developer")
              .set_skills(["Python"])
              .set_seniority("senior")
              .build())
        
        assert isinstance(dev, Developer)
        assert dev.calculate_salary() == 10000
    
    def test_builder_missing_required_field(self):
        with pytest.raises(ValueError):
            (EmployeeBuilder()
            .set_id(1)
            .set_name("Test")
            .build())
    
    def test_builder_chaining(self):
        builder = EmployeeBuilder()
        emp = (builder
               .set_id(1)
               .set_name("John")
               .set_department("IT")
               .set_base_salary(5000)
               .build())
        assert emp is not None


class TestFactoryMethod:
    
    def test_factory_creates_correct_type(self):
        from source_code import EmployeeFactory
        factory = EmployeeFactory()
        emp = factory.create_employee(
            "employee",
            id=1,
            name="John",
            department="IT",
            base_salary=5000
        )
        assert isinstance(emp, Employee)
        assert not isinstance(emp, Manager)
    
    def test_factory_creates_manager(self):
        from source_code import EmployeeFactory
        factory = EmployeeFactory()
        mgr = factory.create_employee(
            "manager",
            id=1,
            name="John",
            department="MGMT",
            base_salary=5000,
            bonus=1000
        )
        assert isinstance(mgr, Manager)

class TestAdapterPattern:
    
    def test_salary_adapter(self):
        emp = Employee(1, "John", "IT", 5000)
        adapter = SalaryAdapter(emp)
        assert adapter.get_monthly_salary() > 0


class TestDecoratorPattern:

    def test_bonus_decorator(self):
        emp = Employee(1, "John", "IT", 5000)
        decorated = BonusDecorator(emp, 1000)
        salary = decorated.calculate_salary()
        assert salary == 6000
    
    def test_multiple_decorators(self):
        emp = Employee(1, "John", "IT", 5000)
        decorated = (BonusDecorator(BonusDecorator(emp, 500), 1000))
        assert decorated.calculate_salary() == 6500

class TestObserverPattern:
    
    def test_observer_pattern_with_mock(self):
        emp = Employee(1, "John", "IT", 5000)
        observer = Mock()
        emp.add_observer(observer)
        emp.notify_observers("salary_changed")
        observer.update.assert_called()
        observer.update.assert_called_with(emp, "salary_changed")
    
    def test_multiple_observers(self):
        emp = Employee(1, "John", "IT", 5000)
        observer1 = Mock()
        observer2 = Mock()
        emp.add_observer(observer1)
        emp.add_observer(observer2)
        emp.notify_observers("status_changed")
        observer1.update.assert_called()
        observer2.update.assert_called()