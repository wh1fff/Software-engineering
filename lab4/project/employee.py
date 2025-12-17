class Employee:
    def __init__(self, id: int, name: str, department: str, base_salary: float):
        self.__id = id
        self.__name = name
        self.__department = department
        self.__base_salary = base_salary
    
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, value):
        if value <= 0:
            raise ValueError('ID должен быть положительным')
        self.__id = value
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        if not value.strip():
            raise ValueError('Имя не может быть пустым')
        self.__name = value
    
    @property
    def base_salary(self):
        return self.__base_salary
    
    @base_salary.setter
    def base_salary(self, value):
        if value <= 0:
            raise ValueError('Зарплата должна быть положительной')
        self.__base_salary = value

    def __str__(self) -> str:
        return f"Сотрудник [id: {self.__id}, имя: {self.__name}, отдел: {self.__department}, базовая зарплата: {self.__base_salary}]"

emp = Employee(1, "Иван Иванов", "Бухгалтерия", 50000)
print(emp)
