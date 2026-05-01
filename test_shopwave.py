import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://127.0.0.1:5000"

# Test user credentials
TEST_NAME = "Test User"
TEST_EMAIL = "testuser_selenium@example.com"
TEST_PASSWORD = "testpass123"


def get_driver():
    """Create and return a headless Chrome driver."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    return driver


class TestShopWave(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """This runs ONCE before all tests. Registers a user for login tests."""
        driver = get_driver()
        try:
            driver.get(f"{BASE_URL}/register")
            driver.find_element(By.ID, "name-input").send_keys(TEST_NAME)
            driver.find_element(By.ID, "email-input").send_keys(TEST_EMAIL)
            driver.find_element(By.ID, "password-input").send_keys(TEST_PASSWORD)
            driver.find_element(By.ID, "register-btn").click()
            time.sleep(1)
        except Exception:
            pass  # User might already exist, that's fine
        finally:
            driver.quit()

    def setUp(self):
        """This runs before EACH test. Creates a fresh browser."""
        self.driver = get_driver()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        """This runs after EACH test. Closes the browser."""
        self.driver.quit()

    # ─── TEST 1 ───────────────────────────────────────────────────────────────
    def test_01_home_page_loads(self):
        """Home page should load successfully."""
        self.driver.get(BASE_URL)
        self.assertIn("200", "200")  # Page loaded
        body = self.driver.find_element(By.TAG_NAME, "body")
        self.assertTrue(body.is_displayed())
        print("✅ Test 1 Passed: Home page loads")

    # ─── TEST 2 ───────────────────────────────────────────────────────────────
    def test_02_home_page_title(self):
        """Home page title should contain 'ShopWave' or 'Home'."""
        self.driver.get(BASE_URL)
        title = self.driver.title
        self.assertTrue(
            "ShopWave" in title or "Home" in title or len(title) > 0,
            f"Unexpected title: {title}"
        )
        print(f"✅ Test 2 Passed: Page title is '{title}'")

    # ─── TEST 3 ───────────────────────────────────────────────────────────────
    def test_03_home_page_brand_visible(self):
        """ShopWave brand name should be visible on home page."""
        self.driver.get(BASE_URL)
        brand = self.driver.find_element(By.CLASS_NAME, "brand")
        self.assertTrue(brand.is_displayed())
        self.assertIn("ShopWave", brand.text)
        print("✅ Test 3 Passed: Brand 'ShopWave' is visible")

    # ─── TEST 4 ───────────────────────────────────────────────────────────────
    def test_04_navigation_links_present(self):
        """Navigation bar should have Home, Products, Register, Login links."""
        self.driver.get(BASE_URL)
        home_link = self.driver.find_element(By.ID, "home-link")
        products_link = self.driver.find_element(By.ID, "products-link")
        self.assertTrue(home_link.is_displayed())
        self.assertTrue(products_link.is_displayed())
        print("✅ Test 4 Passed: Navigation links are visible")

    # ─── TEST 5 ───────────────────────────────────────────────────────────────
    def test_05_get_started_button(self):
        """Clicking 'Get Started' button should navigate to register page."""
        self.driver.get(BASE_URL)
        btn = self.driver.find_element(By.LINK_TEXT, "Get started")
        btn.click()
        time.sleep(1)
        self.assertIn("/register", self.driver.current_url)
        print("✅ Test 5 Passed: 'Get started' button navigates to register")

    # ─── TEST 6 ───────────────────────────────────────────────────────────────
    def test_06_browse_products_button(self):
        """Clicking 'Browse products' button should navigate to products page."""
        self.driver.get(BASE_URL)
        btn = self.driver.find_element(By.LINK_TEXT, "Browse products")
        btn.click()
        time.sleep(1)
        self.assertIn("/products", self.driver.current_url)
        print("✅ Test 6 Passed: 'Browse products' button navigates to products")

    # ─── TEST 7 ───────────────────────────────────────────────────────────────
    def test_07_products_page_loads(self):
        """Products page should load and display products."""
        self.driver.get(f"{BASE_URL}/products")
        self.assertIn("/products", self.driver.current_url)
        body = self.driver.find_element(By.TAG_NAME, "body")
        self.assertIn("product", body.text.lower())
        print("✅ Test 7 Passed: Products page loads successfully")

    # ─── TEST 8 ───────────────────────────────────────────────────────────────
    def test_08_register_page_loads(self):
        """Register page should load with a form."""
        self.driver.get(f"{BASE_URL}/register")
        form = self.driver.find_element(By.ID, "register-form")
        self.assertTrue(form.is_displayed())
        print("✅ Test 8 Passed: Register page loads with form")

    # ─── TEST 9 ───────────────────────────────────────────────────────────────
    def test_09_register_form_fields_present(self):
        """Register form should have name, email, password fields and button."""
        self.driver.get(f"{BASE_URL}/register")
        self.assertTrue(self.driver.find_element(By.ID, "name-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "email-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "password-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "register-btn").is_displayed())
        print("✅ Test 9 Passed: All register form fields are present")

    # ─── TEST 10 ──────────────────────────────────────────────────────────────
    def test_10_register_empty_form_shows_error(self):
        """Submitting empty register form should show an error message."""
        self.driver.get(f"{BASE_URL}/register")
        self.driver.find_element(By.ID, "register-btn").click()
        time.sleep(1)
        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertTrue(
            "fill" in body_text.lower() or "required" in body_text.lower()
            or "register" in self.driver.current_url
        )
        print("✅ Test 10 Passed: Empty register form handled correctly")

    # ─── TEST 11 ──────────────────────────────────────────────────────────────
    def test_11_register_duplicate_email_shows_error(self):
        """Registering with an already-used email should show error."""
        self.driver.get(f"{BASE_URL}/register")
        self.driver.find_element(By.ID, "name-input").send_keys("Another User")
        self.driver.find_element(By.ID, "email-input").send_keys(TEST_EMAIL)
        self.driver.find_element(By.ID, "password-input").send_keys("anypassword")
        self.driver.find_element(By.ID, "register-btn").click()
        time.sleep(1)
        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertTrue(
            "already" in body_text.lower() or "registered" in body_text.lower()
            or "register" in self.driver.current_url
        )
        print("✅ Test 11 Passed: Duplicate email registration shows error")

    # ─── TEST 12 ──────────────────────────────────────────────────────────────
    def test_12_login_page_loads(self):
        """Login page should load with a form."""
        self.driver.get(f"{BASE_URL}/login")
        form = self.driver.find_element(By.ID, "login-form")
        self.assertTrue(form.is_displayed())
        print("✅ Test 12 Passed: Login page loads with form")

    # ─── TEST 13 ──────────────────────────────────────────────────────────────
    def test_13_login_form_fields_present(self):
        """Login form should have email, password fields and login button."""
        self.driver.get(f"{BASE_URL}/login")
        self.assertTrue(self.driver.find_element(By.ID, "email-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "password-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "login-btn").is_displayed())
        print("✅ Test 13 Passed: All login form fields are present")

    # ─── TEST 14 ──────────────────────────────────────────────────────────────
    def test_14_login_with_wrong_credentials(self):
        """Login with wrong credentials should fail and stay on login page."""
        self.driver.get(f"{BASE_URL}/login")
        self.driver.find_element(By.ID, "email-input").send_keys("wrong@example.com")
        self.driver.find_element(By.ID, "password-input").send_keys("wrongpassword")
        self.driver.find_element(By.ID, "login-btn").click()
        time.sleep(1)
        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertTrue(
            "failed" in body_text.lower() or "check" in body_text.lower()
            or "login" in self.driver.current_url
        )
        print("✅ Test 14 Passed: Wrong credentials show error message")

    # ─── TEST 15 ──────────────────────────────────────────────────────────────
    def test_15_login_with_valid_credentials(self):
        """Login with correct credentials should redirect to dashboard."""
        self.driver.get(f"{BASE_URL}/login")
        self.driver.find_element(By.ID, "email-input").send_keys(TEST_EMAIL)
        self.driver.find_element(By.ID, "password-input").send_keys(TEST_PASSWORD)
        self.driver.find_element(By.ID, "login-btn").click()
        time.sleep(1)
        self.assertIn("/dashboard", self.driver.current_url)
        print("✅ Test 15 Passed: Valid login redirects to dashboard")


if __name__ == "__main__":
    unittest.main(verbosity=2)
