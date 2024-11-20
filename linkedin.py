from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Initialize the Chrome driver with Service
website = "https://www.linkedin.com/login"
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get(website)

username = driver.find_element(By.XPATH, '//input[@id="username"]')
password = driver.find_element(By.XPATH, '//input[@id="password"]')

username.send_keys('username')
password.send_keys('password')

login_button = driver.find_element(By.XPATH, '//button[@aria-label="Sign in"]')
login_button.click()

# search_button = driver.find_element(By.XPATH, '//button[contains(@class,
# "search-global-typeahead__collapsed-search-button")]/span') search_button.click() search_button.send_keys('phd
# professor') search_button.click() login_box = driver.find_element(By.XPATH, '//div[@class="_6ltg"]//button[
# @id="u_0_5_bX"]')

search_term = input("What you want to search?")
linkedin_search_baseurl = 'https://www.linkedin.com/search/results/people/?keywords='
driver.get(linkedin_search_baseurl + search_term)

# pagination = driver.find_element(By.XPATH, '//ul[@role="list"]')
# pages = pagination.find_elements(By.TAG_NAME, 'li')
# last_page = int(pagination.text)
last_page = 5

book_title = []
book_author = []
book_length = []
current_page = 1

while current_page <= last_page:
    # Implicit Wait
    time.sleep(5)
    # Explicit Wait
    # container = driver.find_element_by_class_name('adbl-impression-container ')
    # container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '(//ul[@role="list"])[1]')))
    container = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "artdeco-card")]//ul[@role="list"]')))
    products = container.find_elements(By.XPATH, './li')
    # products = WebDriverWait(container, ).until(EC.presence_of_all_elements_located((By.XPATH, './li')))

    for product in products:
        book_title.append(product.find_element(By.XPATH, ".//a[contains(@class, 'app-aware-link ')]//span[contains("
                                                         "@dir,'ltr')]//span[contains(@aria-hidden,'true')]").text)
        # print(book_title)

    current_page = current_page + 1
    try:
        next_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Next"]'))
            )
        next_button.click()
        time.sleep(3)
    except:
        pass

df_books = pd.DataFrame({'name': book_title})
print(df_books)

# Save to CSV
df_books = pd.DataFrame({'title': book_title})
df_books.to_csv('prof_name_sourov.csv', index=False)