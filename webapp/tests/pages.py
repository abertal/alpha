from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def w(driver, locator):
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located(locator))
    return element


class Element:
    def __init__(self, value, by=By.ID):
        self.locator = (by, value)

    def __get__(self, obj, obj_type=None):
        return w(obj.drv, self.locator)


class BasePage:
    title = 'Abertal'

    def __init__(self, drv):
        self.drv = drv
        if self.title:
            # Check we are on the right page
            assert self.title == self.drv.title


class Login(BasePage):
    user = Element('id_username')
    password = Element('id_password')
    submit = Element('id_submit')

    def login(self, username, password) -> BasePage:
        self.user.send_keys(username)
        self.password.send_keys(password)
        self.submit.click()
        return Logged(self.drv)


class Logged(BasePage):
    logout_link = Element('id_logout')

    def logout(self) -> BasePage:
        self.logout_link.click()
        return Login(self.drv)
