from py.excel_manager import ExcelWrapper
from py.invoice_manager import InvoiceManager
from py.selenium_manager import SeleniumManager
from py.transaction_handler import TransactionHandler
from py.utils.logger import Logger
from settings import TEMPFILES_PATH
from py.file_cleaner import FileCleaner
import shutil

class Task:
    def __init__(self): pass
    def start(self): pass
    def process(self): pass
    def exception(self, e): pass
    def end(self): pass

class InvoicesTask(Task):
    def __init__(self, excel_path, invoices_dir):
        super().__init__()
        self.excel_path = excel_path
        self.invoices_dir = invoices_dir

    def start(self):
        super().start()
        self.excel = ExcelWrapper(self.excel_path)
        self.invoice_app = InvoiceManager()

    def process(self):
        self.start()
        super().process()
        for row in self.excel.iter_rows():
            try:
                item = self.excel.to_item(row)
                self.invoice_app.handle_data(item)

                if self.invoice_app.closed is False: 
                    invoice_file = row[0].value
                    shutil.move(f"{self.invoices_dir}/{invoice_file}.xlsx", f"{TEMPFILES_PATH}/{invoice_file}.xlsx")
                else:
                    raise Exception("Se ha frenado la ejecución de Invoice App en medio de la iteración.")
            except Exception as e:
                self.exception(e)
                self.end()
                return
        self.end()

    def end(self):
        super().end()
        self.invoice_app.close()

    def exception(self, e):
        super().exception(e)
        Logger.error(f"No se pudo completar la tarea Invoices. {e}")

class CartTask(Task):
    ITEM_SHAPE = {
        0:"nombre",
        1:"modelo",
        2:"color",
        3:"precio",
        4:"cantidad",
        5:"orden"
    }
    EMPTY_FIELDS = {
        "precio": 3,
        "orden": 5
    }

    def __init__(self, driver_path, excel_path):
        super().__init__()
        self.excel_path = excel_path
        self.selenium = SeleniumManager(driver_path)

    def start(self):
        super().start()
        self.excel = ExcelWrapper(self.excel_path)

    def process(self):
        self.start()
        super().process()

        handler = TransactionHandler(self.selenium)

        for row in self.excel.iter_rows():
            try:
                item = self.excel.to_dict(row, CartTask.ITEM_SHAPE)
                item["cantidad"] = int(item["cantidad"])
                result = handler.handle(item["nombre"], item["color"], item["cantidad"])
                self.excel.set_value(row[CartTask.EMPTY_FIELDS["precio"]], result["precio"])
                self.excel.set_value(row[CartTask.EMPTY_FIELDS["orden"]], result["orden"])
                Logger.info(f"Se ha comprado el producto {item} con orden {result['orden']} ")
            except Exception as e:
                Logger.error(f"No se pudo completar la compra del producto o actualización del excel. {e}")
        self.end()

    def end(self):
        super().end()
        self.selenium.end()

class CleanupTask(Task):
    def __init__(self, directory) -> None:
        self.cleaner = FileCleaner(directory)

    def process(self):
        super().process()
        self.cleaner.delete_expired()