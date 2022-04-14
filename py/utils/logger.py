import logging
import os
import datetime
from datetime import date
import glob
from py.utils.date_helpers import date_compare
from settings import LOG_PATH

class LevelFilter(logging.Filter):
    def __init__(self, level):
        super().__init__()
        self.level = level

    def filter(self, record):
        if self.level == record.levelno:
            return True
        return False

class Logger():
    _initialized = False

    @staticmethod
    def initialize(filename ="LOG.log", levels=[], min_level = logging.DEBUG):
        if Logger._initialized:
            raise Exception("Logger already initialized.")
        today = datetime.date.today()
        Logger._manage_folders()
            
        logpath = f"logs/{today}"

        logging.basicConfig(
            filename=f"{logpath}/{filename}",
            level=min_level,
            format="%(levelname)s : %(asctime)s - %(message)s"
        )

        Logger._set_handlers(
            logging.Formatter("%(levelname)s : %(asctime)s - %(message)s"),
            logpath,
            levels
        )

        Logger._initialized = True

    @staticmethod
    def _manage_folders(most_days = 31):
        today = datetime.date.today()

        try:
            os.mkdir(f"{LOG_PATH}/{today}")
        except Exception as e:
            print(f"Directory {LOG_PATH}/{today} already exists", e)

        logs = glob.iglob(f"{LOG_PATH}/*")
        
        for date_folder in logs:
            try:
                date_folder = date_folder.replace(f"{LOG_PATH}\\", "")
                days = date_compare(today, date.fromisoformat(date_folder))

                if days > most_days:
                    os.rmdir(f"{LOG_PATH}/{date_folder}")
            except ValueError as e:
                print("Formato de fecha inválido.", e)


    @staticmethod
    def _set_handlers(formatter,logpath,levels):
        if formatter is None:
            formatter = logging.Formatter("%(levelname)s : %(asctime)s - %(message)s")
        for level in levels:
            handler = logging.FileHandler(f"{logpath}/{level}.log")
            handler.addFilter(LevelFilter(Logger.level_to_int(level)))
            handler.setFormatter(formatter)
            logging.getLogger().addHandler(handler)

    @staticmethod
    def level_to_int(level_str):
        levels = {
            "DEBUG":logging.DEBUG,
            "INFO":logging.INFO,
            "WARNING":logging.WARNING,
            "ERROR":logging.ERROR,
            "CRITICAL":logging.CRITICAL
        }
        return levels.get(level_str, level_str)

    @staticmethod
    def debug(msg):
        if Logger._initialized is False: Logger.initialize()
        logging.debug(msg)
    
    @staticmethod
    def info(msg):
        if Logger._initialized is False: Logger.initialize()
        logging.info(msg)

    @staticmethod
    def warning(msg):
        if Logger._initialized is False: Logger.initialize()
        logging.warning(msg)

    @staticmethod
    def error(msg):
        if Logger._initialized is False: Logger.initialize()
        logging.error(msg)

    @staticmethod
    def critical(msg):
        if Logger._initialized is False: Logger.initialize()
        logging.critical(msg)