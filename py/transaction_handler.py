from py.utils.logger import Logger
from settings import EMAIL, PASS, BUDGET

class TransactionHandler:
    def __init__(self, selenium):
        self.selenium = selenium
        self.logged_in = False

        self.login()

    @staticmethod
    def _get_taxed_price(price):
        SHIPPING = 2
        TAX = 1.04
        return (price + SHIPPING)*TAX

    def buy_product(self, name, color, amount = 1) -> str:
        self.selenium.goto("http://automationpractice.com/index.php?id_category=3&controller=category")

        product = self.selenium.xpath(f'//*[@class="product-container"][.//a[contains(text(), "{name}")]]//a[contains(@href, "{color}")]')

        if product: product.click()
        else: raise Exception(f"Producto {name} color {color} no encontrado")

        price = float(self.selenium.xpath('//*[@id="our_price_display"]').text.replace("$", ""))
        units_pending = 0

        for i in range(amount -1):
            if self._get_taxed_price(price * (i+1)) < BUDGET:
                self.selenium.xpath('//*[@id="quantity_wanted_p"]/a[span/i[@class="icon-plus"]]').click()
            else:
                Logger.warning(f"La compra de {amount} {name} ({amount*price}) excede el limite de {BUDGET} y fue segmentada.")
                units_pending = amount - (i+1)
                break

        self.selenium.xpath('//*[@id="add_to_cart"]/button').click()
        return {"price":price, "pending":units_pending}

    def handle(self, name, color, amount, _prev_order = ""):
        buy_result = self.buy_product(name, color, amount)
        self.goto_cart()
        order = f"{_prev_order}{self.checkout()}"
        if buy_result["pending"] > 0: return self.handle(name, color, buy_result['pending'], f"{order},")
        return {"orden":order, "precio":buy_result["price"]}

    def goto_cart(self):
        self.selenium.xpath_clickable('//*[@id="layer_cart"]//a[contains(@title, "checkout")]').click()

    def login(self):
        if self.logged_in is False:
            self.selenium.goto("http://automationpractice.com/index.php?controller=authentication&back=my-account")
            self.selenium.xpath('//input[@id="email"]').send_keys(EMAIL)
            self.selenium.xpath('//input[@id="passwd"]').send_keys(PASS)
            self.selenium.xpath('//*[@id="center_column"]//button[@name="SubmitLogin"]').click()
            self.logged_in = True

    def _extract_order(self, text):
        text = text.split("order reference ")[1]
        text = text.split(" in the subject")[0]
        return text

    def checkout(self) -> str:
        self.selenium.xpath('//*[@id="columns"]//a[span[contains(text(),"checkout")]]').click() #cart-checkout
        self.selenium.xpath('//*[@id="center_column"]//button[span[contains(text(),"checkout")]]').click() #adress
        self.selenium.xpath('//*[@id="cgv"]').click()
        self.selenium.xpath('//*[@id="center_column"]//button[span[contains(text(),"checkout")]]').click() #shipping
        self.selenium.xpath('//a[@class="bankwire"]').click() #payment
        self.selenium.xpath('//*[@id="cart_navigation"]//button[@type="submit"][*[contains(text(), "confirm")]]').click()

        return self._extract_order(self.selenium.xpath('//*[@class="box"]').text)
        