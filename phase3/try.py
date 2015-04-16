from selenium import webdriver
import unittest

class GoogleTestCase(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.addCleanup(self.browser.quit)

	def test_page_title(self):
		self.browser.get('http://www.google.com')
		self.assertIn('Google', self.browser.title)

# if __name__ == '__main__':
# 	unittest.main(verbosity=2)
suite = unittest.TestLoader().loadTestsFromTestCase(GoogleTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)