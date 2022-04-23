from py.utils.logger import Logger
from py.tasks import InvoicesTask, CartTask, CleanupTask
from settings import INVOICES_EXCEL_PATH, ALL_INVOICES_PATH, MIN_LOG_LEVEL, CHROME_DRIVER_PATH, PRODUCTS_EXCEL_PATH, TEMPFILES_PATH

Logger.initialize(min_level= MIN_LOG_LEVEL)

try:
    invoice_task = InvoicesTask(INVOICES_EXCEL_PATH, ALL_INVOICES_PATH)
    invoice_task.process()
except Exception as e:
    Logger.critical(f"Error crítico al ejecutar tarea de Invoices. {e}")

try:
    cart_task = CartTask(CHROME_DRIVER_PATH, PRODUCTS_EXCEL_PATH)
    cart_task.process()
except Exception as e:
    Logger.critical(f"Error crítico al ejecutar tarea de compras. {e}")

try:
    cleanup_task = CleanupTask(TEMPFILES_PATH)
    cleanup_task.process()
except Exception as e:
    Logger.critical(f"Error crítico al ejecutar tarea de limpieza. {e}")