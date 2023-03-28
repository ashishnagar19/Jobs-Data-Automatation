from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import os
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
# set up the Chrome driver
driver = webdriver.Firefox()

# navigate to the LinkedIn login page
driver.get("https://www.linkedin.com/login")
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
PASS_INPUT = os.environ.get("PASSWORD")
EMAIL_INPUT = os.environ.get("EMAIL")
# enter your login credentials and submit
email = driver.find_element(by=By.ID, value="username")
password = driver.find_element(by=By.ID, value="password")
email.send_keys(EMAIL_INPUT)
password.send_keys(PASS_INPUT)
password.submit()

time.sleep(15)

email = driver.find_element(by=By.ID, value="username")
password = driver.find_element(by=By.ID, value="password")
email.send_keys(EMAIL_INPUT)
password.send_keys(PASS_INPUT)
password.submit()

# navigate to the LinkedIn jobs page
driver.get("https://www.linkedin.com/jobs")
time.sleep(5)
# search for "software engineer" jobs
search_box = driver.find_element(by=By.XPATH, value="/html/body/div[5]/header/div/div/div/div[2]/div[2]/div/div/input[1]")
search_box.send_keys("node js developer")
# wait for the page to load
time.sleep(5)

# click on "All filters" to refine the search
filter_button = driver.find_element(by=By.XPATH, value="/html/body/div[5]/header/div/div/div/div[2]/div[3]/div/div/input[1]")
filter_button.send_keys("India")
time.sleep(5)
# submit_button = driver.find_element(by=By.XPATH, value="/html/body/div[5]/header/div/div/div/div[2]/button[1]")
filter_button.send_keys(Keys.ENTER)

# wait for the filters to load
time.sleep(10)

# get the list of job openings
job_listings = driver.find_elements(by=By.CLASS_NAME, value="jobs-search-results__list-item")

# create an empty list to store the results
results = []

print(job_listings)

time.sleep(10)

for index, job_listing in enumerate(job_listings):
    try:
        job_title = job_listing.find_element(by=By.XPATH, value=f"/html/body/div[5]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li[{index + 1}]/div/div[1]/div[1]/div[2]/div[1]/a").text
        company_name = job_listing.find_element(by=By.XPATH, value=f"/html/body/div[5]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li[{index + 1}]/div/div[1]/div[1]/div[2]/div[2]/div").text
        job_location = job_listing.find_element(by=By.XPATH, value=f"/html/body/div[5]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li[{index + 1}]/div/div[1]/div[1]/div[2]/div[3]/ul/li[1]").text
        job_link = job_listing.find_element(by=By.XPATH, value=f"/html/body/div[5]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li[{index + 1}]/div/div[1]/div[1]/div[2]/div[1]/a").get_attribute("href")
    except NoSuchElementException:
        pass
    results.append({
        "Job Title": job_title,
        "Company Name": company_name,
        "Location": job_location,
        "Link": job_link
    })

# create a Pandas dataframe to store the results
df = pd.DataFrame(results)

# save the results to a CSV file
df.to_csv("software_engineer_jobs.csv", index=False)

for job in results:
    driver.get(job.Link)
    time.sleep(5000)

# close the Chrome driver


