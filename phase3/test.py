from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Firefox()

browser.get('https://app4.com/admin/status.php?op=del&status_id=2')

print browser.title

# inputElement = browser.find_element_by_name('q')

# inputElement.send_keys('cheese')

# inputElement.submit()

# try:

# 	WebDriverWait(browser, 10).until(EC.title_contains('cheese'))

# 	print browser.title

# finally:
# 	browser.quit()
