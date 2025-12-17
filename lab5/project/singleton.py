class DatabaseConnection:
    _instance: "DatabaseConnection" | None = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection = None
        return cls._instance

    def get_connection(self) -> str:
        if self._connection is None:
            self._connection = "sqlite:///company.db"
        return self._connection
