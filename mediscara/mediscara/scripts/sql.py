import dataclasses
from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from functools import wraps
from typing import ClassVar, Type, List, Tuple, Any

import mysql.connector
from mysql.connector import MySQLConnection, CMySQLConnection
from mysql.connector.errors import ProgrammingError, DatabaseError

try:
    from .logger import Logger
except ImportError:
    from logger import Logger


class Decorator:
    SQL_ATTR = 'sql_method'
    logger = Logger(parent=None, tag="SQL")

    @staticmethod
    def wrap_sql_methods(cl):
        for key in dir(cl):
            value = getattr(cl, key)
            if hasattr(value, Decorator.SQL_ATTR):
                wrapped = Decorator.sql_decorator(value)
                setattr(cl, key, wrapped)

        return cl

    @staticmethod
    def sql_method(func):
        setattr(func, Decorator.SQL_ATTR, True)

        return func

    @staticmethod
    def sql_decorator(func):
        """Wraps the method in a try except case"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)

                return result
            except (DatabaseError, ProgrammingError) as e:
                Decorator.logger.warn(f"SQL Error in {func.__name__}: {str(e)}")
                return SQLServerDisconnectedError()

        return wrapper


# region SQL Error
class SQLError(Exception):
    def __init__(self, text: str):
        super(SQLError, self).__init__(text)


class SQLServerDisconnectedError(SQLError):
    def __init__(self):
        super(SQLServerDisconnectedError, self).__init__("Server disconnected")


class SQLTableNotExistsError(SQLError):
    def __init__(self):
        super(SQLTableNotExistsError, self).__init__("Table does not exist")


class SQLInvalidTableNameError(SQLError):
    def __init__(self):
        super(SQLInvalidTableNameError, self).__init__("Invalid table name")
# endregion


# region Data Classes
@dataclass
class SQLDataClass(ABC):
    """Abstract base data class for storing and retrieving information from a MySQL database"""

    class Timestamp(ABC):
        """Data class for storing timestamp information"""
        FORMAT = "%Y-%m-%d %H:%M:%S"

        @classmethod
        def now(cls):
            """Creates a timestamp instance from the current time"""
            return datetime.now().strftime(cls.FORMAT)

        @classmethod
        def from_datetime(cls, dt: datetime):
            return dt.strftime(cls.FORMAT)

        @classmethod
        def from_string(cls, s: str):
            try:
                return datetime.strptime(s, cls.FORMAT)
            except ValueError:
                print("Invalid string date format")
                return cls.now()

    PYTHON_SQL_DATA_TYPES: ClassVar[dict] = {
        int.__name__: 'integer',
        str.__name__: 'varchar(20)',
        bool.__name__: 'bool',
        Timestamp.__name__: 'timestamp'
    }
    COL_ID: ClassVar[str] = 'id'

    id: str = Timestamp.now()
    in_production: bool = False
    remaining: int = 0

    @classmethod
    def from_query(cls, query_result: tuple):
        data = cls()
        for i, (field_name, field_type) in enumerate(zip(cls.field_names(), cls.field_types())):
            setattr(data, f'{field_name}', field_type(query_result[i]))

        return data

    @classmethod
    def map_data_types(cls):
        """Maps the field types to their MySQL representation"""
        data_list = list()
        for field_ in dataclasses.fields(cls):
            data_list.append((field_.name, cls.PYTHON_SQL_DATA_TYPES[field_.type.__name__]))

        return data_list

    @classmethod
    def field_names(cls) -> List[str]:
        """Returns the field names of this class"""
        return [field_.name for field_ in dataclasses.fields(cls)]

    @classmethod
    def field_types(cls) -> List[Type[str]]:
        """Returns the field types as strings"""
        return [field_.type for field_ in dataclasses.fields(cls)]

    def values(self):
        """Returns the field values"""
        values = list()
        for field_ in dataclasses.astuple(self):
            if isinstance(field_, tuple):
                values.append(f"'{field_[0]}'")

            elif isinstance(field_, str):
                values.append(f"'{field_}'")  # add quotation marks
            else:
                values.append(str(field_))
        return values

    def sql_values(self):
        values = list()
        for field_ in dataclasses.astuple(self):
            if isinstance(field_, bool):
                values.append(str(int(field_)))

            elif isinstance(field_, str):
                values.append(f"'{field_}'")  # add quotation marks

            else:
                values.append(str(field_))

        return values


@dataclass
class Bell(SQLDataClass):
    """Dataclass for storing information about a bell order"""

    type: str = ""
    count: int = 0


@dataclass
class Cell2Data(SQLDataClass):
    """Dataclass for storing information about the working orders in robotic cell 2"""

    """ FIELDS """
    inc_type: str = ""  # incubator type
    part_type: str = ""  # part type
    marker_count: int = 0  # count of parts to be marked
# endregion


@Decorator.wrap_sql_methods
class SQLManager:
    HOST = "localhost"
    USER = "user"
    PASSWORD = "user"

    COL_ID = "id"

    # def __init__(self, data: Type[SQLDataClass], table_name: str):
    #     self.logger = Logger(None)
    #
    #     self.__data_model = data
    #     self.__table_name = table_name
    #
    #     self.__db = None  # type: Union[CMySQLConnection, MySQLConnection] or None
    #
    #     self.__connected = False

    def __init__(self, table: List[Tuple[str, Type[SQLDataClass]]]):
        self.logger = Logger(None, tag="SQL")
        Logger.LOG_LEVEL = Logger.INFO

        self.__data_models = dict()
        for dm in table:
            self.__data_models[dm[0]] = dm[1]  # map the table names as keys to the data types as values

        self.__db = None

        self.__connected = False

    def connect_to_database(self):
        """Attempts to connect to the MySQL database"""
        try:
            self.__db = mysql.connector.connect(
                host=self.HOST,
                user=self.USER,
                password=self.PASSWORD,
                database="db"
            )

        except ProgrammingError as e:
            raise e

        except DatabaseError:
            msg = "Could not connect to database, retrying"
            return False, msg

        else:
            msg = f"Connected to database as '{self.USER}'"
            self.__connected = True
            self._check_table()

            # set isolation level
            assert isinstance(self.__db, (CMySQLConnection, MySQLConnection))
            cursor = self.__db.cursor()
            cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")
            cursor.close()
            self.__db.commit()

            return True, msg

    def close(self):
        """Closes the connection to the SQL database"""
        if self.__db is not None:
            self.logger.info("Closing sql connection")
            self.__db.close()

    def _check_table(self):
        """Check if the table exists in the given database"""

        for table_name in self.__data_models.keys():
            sql = f"SHOW TABLES LIKE '%{table_name}%'"
            cursor = self.__db.cursor()
            cursor.execute(sql)

            if not cursor.fetchall():  # empty list -> no such table
                self.logger.info(f"{table_name} not in the database, creating table")
                self._create_table(table_name)

            cursor.close()

    @Decorator.sql_method
    def _create_table(self, table_name: str):
        """Creates a new MySQL table"""

        assert isinstance(self.__db, (CMySQLConnection, MySQLConnection))
        sql = f'CREATE TABLE {table_name} ('

        dm = self.dm(table_name)  # type: Type[SQLDataClass]

        for column_name, column_type in dm.map_data_types():
            assert isinstance(column_name, str), isinstance(column_type, str)

            if column_name == self.COL_ID:
                sql += f'{column_name.upper()} {column_type.upper()} PRIMARY KEY, '

            else:
                sql += f'{column_name.upper()} {column_type.upper()}, '

        sql = sql[:-2] + ");"
        print(sql)

        cursor = self.__db.cursor()
        cursor.execute(sql)
        self.__db.commit()
        cursor.close()

    @Decorator.sql_method
    def get_next_element(self, table_name: str):
        """Returns the first element ordered by the id value"""
        assert isinstance(self.__db, (CMySQLConnection, MySQLConnection))

        dm = self.dm(table_name)
        if dm is None:
            return SQLTableNotExistsError()

        columns_string = ', '.join(column for column in dm.field_names())

        sql = f"SELECT {columns_string} FROM {table_name} ORDER BY {self.COL_ID} LIMIT 1"
        cursor = self.__db.cursor()
        cursor.execute(sql)

        result = cursor.fetchall()
        cursor.close()

        if not result:  # emtpy list
            self.logger.debug("Empty query result")
            return None

        result = result[0]

        return dm.from_query(result)

    @Decorator.sql_method
    def get_element(self, id_: str, table_name: str) -> SQLDataClass or None:
        assert isinstance(self.__db, (CMySQLConnection, MySQLConnection))
        dm = self.dm(table_name)

        if dm is None:
            return SQLTableNotExistsError()

        columns_string = ', '.join(column for column in dm.field_names())

        sql = f"SELECT {columns_string} FROM {table_name} WHERE {self.COL_ID} = '{id_}' ORDER BY {self.COL_ID}"
        cursor = self.__db.cursor()
        cursor.execute(sql)

        result = cursor.fetchall()
        cursor.close()

        if not result:  # emtpy list
            self.logger.debug("Empty query result")
            return None

        result = result[0]  # get the element from the one element list

        return self.__data_model.from_query(result)

    @Decorator.sql_method
    def get_all_elements(self, table_name: str) -> List[SQLDataClass] or None:
        assert isinstance(self.__db, (CMySQLConnection, MySQLConnection))
        dm = self.dm(table_name)

        if dm is None:
            return SQLTableNotExistsError()

        columns_string = ', '.join(column for column in dm.field_names())

        sql = f"SELECT {columns_string} FROM {table_name} ORDER BY {self.COL_ID}"
        cursor = self.__db.cursor()
        cursor.execute(sql)

        results = cursor.fetchall()
        cursor.close()

        if not results:  # empty list
            self.logger.debug("Empty query result")
            return []

        data_list = list()
        for result in results:
            data_list.append(dm.from_query(result))

        return data_list

    @Decorator.sql_method
    def insert_element(self, data: SQLDataClass, table_name: str) -> bool:
        """Attempts to insert a new element into the database"""
        assert isinstance(self.__db, (CMySQLConnection, MySQLConnection))

        dm = self.dm(table_name)

        if dm is None:
            self.logger.warn(str(SQLTableNotExistsError()))
            return False

        sql = f"INSERT INTO {table_name} ({', '.join(dm.field_names())}) VALUES ({', '.join(data.sql_values())})"
        cursor = self.__db.cursor()
        cursor.execute(sql)
        cursor.close()
        self.__db.commit()

        if cursor.rowcount != 1:
            self.logger.warn("Unsuccessful insert attempt")

            return False

        return True

    @Decorator.sql_method
    def delete_element(self, id_: str, table_name: str):
        """Attempts to delete an element from the database"""
        assert isinstance(self.__db, (CMySQLConnection, MySQLConnection))

        dm = self.dm(table_name)

        if dm is None:
            return SQLTableNotExistsError()

        sql = f"DELETE FROM {table_name} WHERE {self.COL_ID} = '{id_}'"
        cursor = self.__db.cursor()
        cursor.execute(sql)
        self.__db.commit()

        success = cursor.rowcount == 1

        cursor.close()

        return success

    @Decorator.sql_method
    def delete_elements(self, ids: List[str], table_name: str):
        assert isinstance(self.__db, (CMySQLConnection, MySQLConnection))

        dm = self.dm(table_name)

        if dm is None:
            return SQLTableNotExistsError()

        ids = [f"'{id_}'" for id_ in ids]

        self.logger.debug(f"Deleting item(s) with id: {', '.join(ids)}")

        sql = f"DELETE FROM {table_name} WHERE {self.COL_ID} IN ({', '.join(ids)})"
        self.logger.debug(sql)

        cursor = self.__db.cursor()
        cursor.execute(sql)
        self.__db.commit()

        success = cursor.rowcount == len(ids)

        cursor.close()

        return success

    @Decorator.sql_method
    def update_element(self, table_name: str, new_value: SQLDataClass):
        """Updates the selected element in the database"""
        assert isinstance(self.__db, (CMySQLConnection, MySQLConnection))

        try:
            data_models = self.__data_models.values()  # list of data model classes
            assert isinstance(new_value, tuple(data_models))

        except AssertionError:
            self.logger.warn(f"{__name__}: Invalid class for update: {new_value.__class__.__name__}")

        if isinstance(new_value, str):
            new_value = f"'{new_value}'"  # add quotation marks

        sql = f"UPDATE {table_name} SET "
        field_names = new_value.field_names()

        id_ = ""
        for name, value in zip(field_names, new_value.sql_values()):
            if name == self.COL_ID:
                id_ = value
            else:
                sql += f'{name}={value}, '

        sql = sql[:-2]  # remove the last colon and space
        sql += f" WHERE {self.COL_ID} = {id_}"
        self.logger.debug(sql)

        cursor = self.__db.cursor()
        cursor.execute(sql)
        success = cursor.rowcount == 1
        cursor.close()
        self.__db.commit()

        return success

    def dm(self, table_name: str):
        return self.__data_models.get(table_name)

    @property
    def connected(self):
        return self.__connected


if __name__ == '__main__':
    # sm = SQLManager(Bell, table_name='sc1')
    # sm.connect_to_database()
    # # sm.insert_element(Bell(type="1", count=1))
    # b = sm.get_next_element()
    # print(b)

    print(Cell2Data.field_names())
