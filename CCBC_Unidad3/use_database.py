import psycopg2


class UseDatabase:
    def __init__(self, params: dict) -> None:
        self.params = params
        self.connection = None

    def __enter__(self)->'cursor':
        try:
            self.connection = psycopg2.connect(**self.params)
            self.cursor = self.connection.cursor()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()