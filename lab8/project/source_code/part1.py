class Employee:
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

    def __str__(self):
        return (
            f"сотрудник id: {self.__id}, имя: {self.__name}, отдел: {self.__department}, "
            f"базовая зарплата: {self.__base_salary}"
        )


def main():
    emp = Employee(1, "Travis Smith", "IT", 500)
    print(str(emp))
    print(emp.id)
    print(emp.name)

# demo вызова исключения

    #emp.id = -1
    #emp.base_salary = -1
    #emp.name = ""
    #emp.department = ""

if __name__ == "__main__":
    main()
