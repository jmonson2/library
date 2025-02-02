import sqlite3
import logging
from pathlib import Path
from util.paths import Paths

class Initialize:

    def __init__(self) -> None:
        self.paths = Paths()
        self.logger: logging.Logger = logging.getLogger(name=__name__)


    def initialize(self) -> bool:
        return (
            self.__initialize_logs() and
            self.__initialize_database() and
            self.__initialize_imports() and
            self.__initialize_completed_imports()
        )


    def __initialize_database(self) -> bool:
        success: bool = False
        if Path.exists(self.paths.db_file_path):
            self.logger.debug(f"Database file exists in {self.paths.db_file_path}")
            success = True
            return success
        Path.mkdir(self=self.paths.db_path, parents=True, exist_ok=True)
        Path.touch(self.paths.db_file_path)
        self.logger.info(msg="Initializing Database")
        con: sqlite3.Connection = sqlite3.connect(self.paths.db_file_path)
        create_books_sql: str = "create table books(id integer primary key autoincrement, title text not null, \
            author text not null, available text not null, date_created text not null, check_in_date text, \
            check_out_date text);"
        try:
            _ = con.execute(create_books_sql)
            con.commit()
            self.logger.info(f"sqlite database created in {self.paths.db_file_path}")
            success = True
        except Exception as e:
            con.rollback()
            Path.unlink(self.paths.db_file_path)
            self.logger.error(msg=f"Failed to Intialize Database in {self.paths.db_file_path}: {repr(e)}")
        finally:
            con.close()
            return success


    def __initialize_logs(self) -> bool:
        success: bool = False
        try:
            if not Path.exists(self.paths.log_path):
                Path.mkdir(self=self.paths.log_path, parents=True)
            logging.basicConfig(
                filename=self.paths.log_file_path,
                encoding="utf-8",
                filemode="a",
                format="{asctime} - {levelname} - {funcName} - {lineno} - {message}",
                style="{",
                datefmt="%Y-%m-%d %H:%M",
                level=logging.DEBUG)
            success = True
        except Exception as e:
            success = False
            print(f"Error in intializing logs {repr(e)}")
            _ = input()
        finally:
            return success


    def __initialize_imports(self) -> bool:
        success: bool = False
        try:
            if not Path.exists(self.paths.import_path):
                Path.mkdir(self=self.paths.import_path, parents=True)
                self.logger.info(f"created directory for CSV imports in {self.paths.import_path}")
                success = True
            else:
                success = True
        except Exception as e:
            success = False
            self.logger.error(f"Failed to create imports directory in {self.paths.import_path}: {repr(e)}")
        finally:
            return success
    

    def __initialize_completed_imports(self) -> bool:
        success: bool = False
        try:
            if not Path.exists(self.paths.import_completed_path):
                Path.mkdir(self=self.paths.import_completed_path, parents=True)
                self.logger.info(f"created directory for CSV imports in {self.paths.import_completed_path}")
                success = True
            else:
                success = True
        except Exception as e:
            success = False
            self.logger.error(f"Failed to create completed imports directory in {self.paths.import_completed_path}: {repr(e)}")
        finally:
            return success

