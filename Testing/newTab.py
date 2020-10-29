from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

PATH = 'C:\sdk\chromedriver\chromedriver.exe'
driver = webdriver.Chrome(PATH)
driver.get("http://www.google.com/")

link = 'https://pubmed.ncbi.nlm.nih.gov/31811279/'
# link = link[1:-1]'
# print(link)'

driver.execute_script(f'''window.open("{link}","_blank");''')
time.sleep(2)

driver.switch_to.window(driver.window_handles[0])

time.sleep(2)

driver.switch_to.window(driver.window_handles[1])

# #open tab
# driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't') 
# # You can use (Keys.CONTROL + 't') on other OSs

# # Load a page 
# driver.get('http://stackoverflow.com/')
# # Make the tests...

# # close the tab
# # (Keys.CONTROL + 'w') on other OSs.
# driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w') 


time.sleep(2)
driver.close()