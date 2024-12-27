import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time, test_constants

class IndexPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_a_index_invalid_username(self):        
        driver = self.driver
        driver.get(test_constants.APP_URL)
        self.assertIn("Hydra", driver.title)
        elem = driver.find_element(By.ID, "uname")
        elem.send_keys("test_admin_wrong")
        time.sleep(1)
        elem = driver.find_element(By.ID, "pwd")
        elem.send_keys(test_constants.MAIN_USER_PASSWORD)
        time.sleep(1)
        button = driver.find_element(By.ID, "login")
        button.click()
        time.sleep(1)
        self.assertIn("Invalid Username", driver.page_source)
        
    def test_b_index_invalid_password(self):        
        driver = self.driver
        driver.get(test_constants.APP_URL)
        self.assertIn("Hydra", driver.title)
        elem = driver.find_element(By.ID, "uname")
        elem.send_keys(test_constants.MAIN_USER_NAME)
        time.sleep(1)
        elem = driver.find_element(By.ID, "pwd")
        elem.send_keys("this is total crap")
        time.sleep(1)
        button = driver.find_element(By.ID, "login")
        button.click()
        time.sleep(1)
        self.assertIn("Invalid Username", driver.page_source)

    def test_c_index_valid_info(self):        
        driver = self.driver
        driver.get(test_constants.APP_URL)
        self.assertIn("Hydra", driver.title)
        elem = driver.find_element(By.ID, "uname")
        elem.send_keys(test_constants.MAIN_USER_NAME)
        time.sleep(1)
        elem = driver.find_element(By.ID, "pwd")
        elem.send_keys(test_constants.MAIN_USER_PASSWORD)
        time.sleep(1)
        button = driver.find_element(By.ID, "login")
        button.click()
        time.sleep(1)
        self.assertIn("My Events", driver.page_source)

    def test_d_unverified_user(self):
        driver = self.driver
        driver.get(test_constants.APP_URL)
        self.assertIn("Hydra", driver.title)
        elem = driver.find_element(By.ID, "uname")
        elem.send_keys(test_constants.UNVERIFIED_USER_NAME)
        time.sleep(1)
        elem = driver.find_element(By.ID, "pwd")
        elem.send_keys(test_constants.UNVERIFIED_USER_PASSWORD)
        time.sleep(1)
        button = driver.find_element(By.ID, "login")
        button.click()
        time.sleep(1)
        self.assertIn("Not Verified", driver.page_source)

    def test_e_verify_unverified_user(self):
        driver = self.driver
        driver.get(test_constants.APP_URL)
        self.assertIn("Hydra", driver.title)
        link = driver.find_element(By.ID, "verify")
        link.click()
        time.sleep(1)
        elem = driver.find_element(By.ID, "email")
        elem.send_keys(test_constants.UNVERIFIED_USER_EMAIL)
        elem = driver.find_element(By.ID, "pwd")
        elem.send_keys(test_constants.UNVERIFIED_USER_PASSWORD)
        elem = driver.find_element(By.ID, "code")
        elem.send_keys(test_constants.VERIFICATION_CODE)
        button = driver.find_element(By.ID, "verify")
        button.click()
        self.assertIn("Account Verified", driver.page_source)

    def test_f_verify_unverified_user_is_verified(self):
        driver = self.driver
        driver.get(test_constants.APP_URL)
        self.assertIn("Hydra", driver.title)
        elem = driver.find_element(By.ID, "uname")
        elem.send_keys(test_constants.UNVERIFIED_USER_NAME)
        time.sleep(1)
        elem = driver.find_element(By.ID, "pwd")
        elem.send_keys(test_constants.UNVERIFIED_USER_PASSWORD)
        time.sleep(1)
        button = driver.find_element(By.ID, "login")
        button.click()
        time.sleep(1)
        self.assertIn("My Events", driver.page_source)

    def test_g_verify_links(self):
        driver = self.driver
        driver.get(test_constants.APP_URL)
        self.assertIn("Hydra", driver.title)
        link = driver.find_element(By.ID, "verify")
        link.click()
        time.sleep(1)
        self.assertIn("Verify Account", driver.page_source)
        link = driver.find_element(By.ID, "goback")
        link.click()
        time.sleep(1)
        self.assertIn("Verify Account", driver.page_source)

    def test_h_create_links(self):
        driver = self.driver
        driver.get(test_constants.APP_URL)
        self.assertIn("Hydra", driver.title)
        link = driver.find_element(By.ID, "newUser")
        link.click()
        time.sleep(1)
        self.assertIn("Create New Account", driver.page_source)
        link = driver.find_element(By.ID, "goback")
        link.click()
        time.sleep(1)
        self.assertIn("Verify Account", driver.page_source)

    def test_a_create_user(self):
        driver = self.driver
        driver.get(test_constants.APP_URL)
        self.assertIn("Hydra", driver.title)
        link = driver.find_element(By.ID, "newUser")
        link.click()
        time.sleep(1)
        elem = driver.find_element(By.ID, "email")
        elem.send_keys(test_constants.CREATE_USER_EMAIL)
        elem = driver.find_element(By.ID, "pwd")
        elem.send_keys(test_constants.CREATE_USER_PASSWORD)
        time.sleep(1)
        elem = driver.find_element(By.ID, "cpwd")
        elem.send_keys(test_constants.CREATE_USER_PASSWORD)
        time.sleep(1)
        elem = driver.find_element(By.ID, "uname")
        elem.send_keys(test_constants.CREATE_USER_NAME)
        time.sleep(1)
        button = driver.find_element(By.ID, "create")
        button.click()
        time.sleep(2)
        self.assertIn("Account Creation Successful!", driver.page_source)

    def test_j_create_user_is_created(self):
        driver = self.driver
        driver.get(test_constants.APP_URL)
        self.assertIn("Hydra", driver.title)
        elem = driver.find_element(By.ID, "uname")
        elem.send_keys(test_constants.CREATE_USER_NAME)
        time.sleep(1)
        elem = driver.find_element(By.ID, "pwd")
        elem.send_keys(test_constants.CREATE_USER_PASSWORD)
        time.sleep(1)
        button = driver.find_element(By.ID, "login")
        button.click()
        time.sleep(1)
        self.assertIn("Not Verified", driver.page_source)

    def test_a_create_user_invalid_data(self):
        driver = self.driver
        driver.get(test_constants.APP_URL)
        self.assertIn("Hydra", driver.title)
        link = driver.find_element(By.ID, "newUser")
        link.click()
        time.sleep(1)
        elem = driver.find_element(By.ID, "email")
        elem.send_keys(test_constants.CREATE_USER_EMAIL)
        elem = driver.find_element(By.ID, "pwd")
        elem.send_keys(test_constants.CREATE_USER_PASSWORD)
        time.sleep(1)
        elem = driver.find_element(By.ID, "cpwd")
        elem.send_keys(test_constants.CREATE_USER_PASSWORD)
        time.sleep(1)
        elem = driver.find_element(By.ID, "uname")
        elem.send_keys("short")
        time.sleep(1)
        button = driver.find_element(By.ID, "create")
        button.click()
        time.sleep(1)
        self.assertIn("Username must be between", driver.page_source)
        elem = driver.find_element(By.ID, "uname")
        elem.clear()
        elem.send_keys(test_constants.CREATE_USER_NAME)
        time.sleep(1)
        elem = driver.find_element(By.ID, "email")
        elem.clear()
        elem.send_keys("not an email")
        button = driver.find_element(By.ID, "create")
        button.click()
        time.sleep(1)
        self.assertIn("Email must follow the pattern of", driver.page_source)
        elem = driver.find_element(By.ID, "email")
        elem.clear()
        elem.send_keys(test_constants.CREATE_USER_EMAIL)
        elem = driver.find_element(By.ID, "cpwd")
        elem.clear()
        elem.send_keys('junk')
        button = driver.find_element(By.ID, "create")
        button.click()
        time.sleep(1)
        self.assertIn("Passwords MUST match", driver.page_source)
        elem = driver.find_element(By.ID, "pwd")
        elem.clear()
        elem.send_keys("junk")
        button = driver.find_element(By.ID, "create")
        button.click()
        time.sleep(1)
        self.assertIn("Password is not strong enough", driver.page_source)
        
    def tearDown(self):
        self.driver.close()
        return super().tearDown()
    
if __name__ == "__main__":
    unittest.main()
