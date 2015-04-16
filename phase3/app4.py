from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Firefox()

browser.get('https://app4.com/')
print browser.title
# log in first
username = browser.find_element_by_name('username')
username.send_keys('admin@admin.com')
password = browser.find_element_by_name('password')
password.send_keys('admin')
password.submit()

# perform operation
browser.get('https://app4.com/admin/status.php?op=del&status_id=2')

browser.quit()