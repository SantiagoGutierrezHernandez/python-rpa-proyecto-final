import os
import glob
import datetime
from py.utils.date_helpers import date_compare
from settings import FILE_LIFETIME_DAYS
from py.utils.logger import Logger

class FileCleaner:
    def __init__(self, directory):
        self.directory = directory

    def delete_expired(self):
        files = glob.iglob(f"{self.directory}/*")
        for file in files:
            last_access = datetime.date.fromtimestamp(os.stat(file).st_atime)
            
            if date_compare(last_access, datetime.date.today()) > FILE_LIFETIME_DAYS:
                try:
                    os.rmdir(file)
                    Logger.info(f"Directorio {file} en carpeta de temporales eliminado (Ultimo acceso: {last_access}).")
                except Exception:
                    os.remove(file)
                    Logger.info(f"Archivo {file} en carpeta de temporales eliminado (Ultimo acceso: {last_access}).")