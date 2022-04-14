from settings import INVOICES_APP_PATH
import subprocess
import pyautogui
import time
from py.utils.date_helpers import prepend_date_zero
from py.utils.logger import Logger

class InvoiceItem:
    def __init__(self, id, name, value, amount, date, num):
        self.id = id
        self.name = name
        self.value = value
        self.amount = amount
        self.subtotal = value * amount
        self.date = date
        self.num = num

    def __str__(self) -> str:
        return f"(Num:{self.num},Nombre: {self.name}, ID:{self.id}, Unidad:{self.value}, Cantidad:{self.amount}, Subtotal:{self.subtotal}, Fecha: {self.date})"

class Field:
    START = 0
    SAVE = 0
    ID = 1
    DATE = 2
    PRODUCTS = 3
    ADD = 4
    REMOVE = 5
    END = 5

    def __init__(self, field = 0):
        self._index = field

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        self._index = value % (Field.END + 1)

class InvoiceManager:
    def __init__(self):
        self.app = subprocess.Popen(INVOICES_APP_PATH)
        self.field = Field()
        self.closed = False
        time.sleep(5)

    def _move_to(self, field_index):
        if self.closed: return
        if field_index < Field.START or field_index > Field.END:
            raise Exception(f"Requested field index ({field_index}) is invalid or out of bounds [{Field.START}, {Field.END}].")
        while self.field.index is not field_index:
            pyautogui.press("tab")
            self.field.index += 1
            time.sleep(0.02)

    def _set_id(self, value):
        if self.closed: return
        self._move_to(Field.ID)
        pyautogui.hotkey("ctrl", "a")
        pyautogui.press("backspace")
        time.sleep(0.02)
        pyautogui.typewrite(value, 0.02)

    def _set_date(self, date):
        if self.closed: return
        datestr = f"{prepend_date_zero(date.day)}/{prepend_date_zero(date.month)}/{date.year}"
        self._move_to(Field.DATE)
        pyautogui.typewrite(datestr, 0.02)

    def _add(self):
        if self.closed: return
        self._move_to(Field.ADD)
        pyautogui.press("enter")
        time.sleep(0.02)

    def _remove(self):
        if self.closed: return
        self._move_to(Field.REMOVE)
        pyautogui.press("enter")
        time.sleep(0.02)

    def _save(self):
        if self.closed: return
        self._move_to(Field.SAVE)
        pyautogui.press("enter")
        time.sleep(0.02)
        pyautogui.press("enter")
        time.sleep(0.02)
        pyautogui.hotkey("shift", "tab")
        self.field.index = Field.START

    def _fill_item_data(self, item):
        if self.closed: return
        self._move_to(Field.PRODUCTS)
        try:
            pyautogui.typewrite(str(item.id), 0.02)
            pyautogui.press("tab")
            pyautogui.typewrite(str(item.name), 0.02)
            pyautogui.press("tab")
            pyautogui.typewrite(str(item.value), 0.02)
            pyautogui.press("tab")
            pyautogui.typewrite(str(item.amount), 0.02)
            pyautogui.press("tab")
            pyautogui.typewrite(str(item.subtotal), 0.02)
            pyautogui.press("tab")
        except Exception as e:
            Logger.error(f"Item de Invoices inválido. {e}")

    def handle_data(self, item):
        if self.closed: return
        try:
            self._set_id(item.num)
            self._set_date(item.date)
            self._add()
            self._fill_item_data(item)
            self._save()
            Logger.info(f"Item agregado exitosamente. {str(item)}")
        except pyautogui.FailSafeException as e:
            Logger.critical(f"Ejecución de PyAutoGui interrumpida. {e}")
            self.close()
        except KeyboardInterrupt as e:
            Logger.critical(f"Ejecución de PyAutoGui interrumpida. {e}")
            self.close()
        except Exception as e:
            Logger.error(f"Item de Invoices inválido. {e}")

    def close(self):
        if self.closed is False:
            time.sleep(1)
            self.app.terminate()
            self.closed = True
            time.sleep(1)
        else:
            Logger.warning("Se ha intentado cerrar múltiples veces InvoiceApp.")