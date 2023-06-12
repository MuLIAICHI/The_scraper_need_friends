from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import json

driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

# Get the website URL : navigate to the website 
driver.implicitly_wait(10)

driver.get("https://www.jobsite.co.uk/")


# Handle cookies 
sleep(2)
cookie = driver.find_element(By.ID, "ccmgt_explicit_accept")

try :
    cookie.click()
except :
    pass


# Handle the boxes for entrinig the keywords for search 

wait = WebDriverWait(driver, 10)

wait.until(EC.presence_of_element_located((By.ID, "keywords")))
job_title = driver.find_element(By.ID, "keywords")
job_title.clear()
job_title.send_keys("Software Engineer")
job_title.send_keys(Keys.RETURN)


wait.until(EC.presence_of_element_located((By.ID, "location")))
location = driver.find_element(By.ID, "location")
location.clear()
location.send_keys("Manchester")
location.send_keys(Keys.RETURN)


wait.until(EC.presence_of_element_located((By.ID, "Radius")))
dropDown = driver.find_element(By.ID, "Radius")
Raduis = Select(dropDown)
Raduis.select_by_visible_text("30 miles")

wait.until(EC.presence_of_element_located((By.ID, "search-button")))
Button = driver.find_element(By.ID, "search-button")
Button.click()
sleep(2)
# Get the data from the first three pages 

# create an empty list to store the data
data = []
for p in range(4):
    wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@data-at='job-item']")))
    Boxes = driver.find_elements(By.XPATH, "//*[@data-at='job-item']")
    with open("data.json", "w") as file:
        for box in Boxes:
            title = box.find_element(By.CSS_SELECTOR, "div.res-j4ov1b > h2.res-hbjkz4").text.strip()
            partnership = box.find_element(By.CSS_SELECTOR, "div.res-j4ov1b > span.res-zr46ku").text.strip()
            company = box.find_element(By.CSS_SELECTOR, "div.res-j4ov1b > div.res-1v262t5 > span.res-1kgfsb7").text.strip()
            data.append({
                "job_title": title,
                "partnership": partnership,
                "company": company
                }
            )
            # write the data into the json file 
            file.write(json.dumps(data))
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Next']")))
        next = driver.find_element(By.XPATH, "//a[@aria-label='Next']")
        next.click()
    json.dump(data, file)
driver.close()