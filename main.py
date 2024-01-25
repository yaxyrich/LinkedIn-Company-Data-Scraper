import variables
import csv
import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from parsel import Selector
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

# Chrome driver install
driver = webdriver.Chrome(executable_path=variables.chrome_driver_path)
print("username: " + variables.my_username)
driver.get('https://www.linkedin.com/')
sleep(2)
#login to LinkedIn
username = driver.find_element(By.ID, 'session_key')
username.send_keys(variables.my_username) # username field
sleep(1)
password = driver.find_element(By.NAME, 'session_password')
password.send_keys(variables.my_password) # password field
sleep(1)
log_in_button = driver.find_element(By.CLASS_NAME,'sign-in-form__submit-btn--full-width') # submit button
log_in_button.click() # click the submit button

home_button = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "app-aware-link")]//span[contains(@title, "Home")]'))
)
print("Log in successful!")

# Load Excel sheet with company names
df_original = pd.read_excel(variables.excel_file_path)

# Create a new DataFrame for the results
df_result = pd.DataFrame(columns=['Company','Industry','Business Summary','Year Founded','Location','Size','Website','LinkedIn URL'])

for index, row in df_original.iterrows():
    # Extract company name from the original Excel sheet
    company_name = row['Company']
    try:
        # Search company in LinkedIn search bar
        try:
            search_bar = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//input[@class="search-global-typeahead__input"]')))
        # exception may raise if search_bar can't be found. One common example is when our chrome tab is not in full screen. Since things are minimized in this case,
        #   only the search icon is present so the previous line will not capture the search bar. We will need to click te search icon first in order for search bar to show up
        except TimeoutException:
            search_icon = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'search-global-typeahead__collapsed-search-button')))
            search_icon.click()
            search_bar = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//input[@class="search-global-typeahead__input"]')))
        search_bar.clear()
        search_bar.send_keys(company_name)  ##company name
        search_bar.send_keys(Keys.ENTER)
        sleep(3)

        # click on the companies tab to filter result
        try: # if "company" filter is already on
            filter_buttons = driver.find_elements(By.XPATH, '//li[@class="search-reusables__primary-filter"]/button[contains(@class, "search-reusables__filter-pill-button")]')
            # Iterate through the buttons to find the one with text "Companies"
            companies_filter_button = None
            for button in filter_buttons:
                if 'Companies' in button.text:
                    companies_filter_button = button
                    break
                    
            if companies_filter_button is not None:
                 # Check if the button is pressed (selected)
                if 'artdeco-pill--selected' in companies_filter_button.get_attribute('class'):
                    print("Companies filter button is already selected.")
                else:
                    # If the button is found but not selected, you can click it to select
                    companies_filter_button.click()
                    print("Clicked Companies filter button to select.")
            else:
                # Check if the dropdown version is present
                dropdown_button = driver.find_element(By.XPATH, '//li[@class="search-reusables__primary-filter"]//button[@aria-label="Filter by: Companies"]')
                
                # Check if the dropdown button is pressed (selected)
                if 'artdeco-pill--selected' in dropdown_button.get_attribute('class'):
                    print("Companies filter button is already selected (dropdown version).")
                else:
                    # If the dropdown button is found but not selected, you can click it to select
                    dropdown_button.click()


        except NoSuchElementException: # needs to filter by "company"
            # company_tab = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Companies"]')))
            # company_tab.click()
            # sleep(2)
            continue

        # click on the toppest search result
        try:
            top_company = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//li[contains(@class, "reusable-search__result-container")]//a[contains(@class, "app-aware-link")]')))
        except TimeoutException: # if there's no company found in search result
            new_row = {'Company':company_name, 'Industry':'', 'Business Summary':'', 'Year Founded':'', 'Location':'', 'Size':'', 'Website':'', 'LinkedIn URL':''}
            df_result = pd.concat([df_result, pd.DataFrame([new_row])], ignore_index=True)
            continue

        # get url
        company_url = driver.find_element(By.XPATH, '//li[contains(@class, "reusable-search__result-container")]//a[contains(@class, "app-aware-link")]').get_attribute('href')
        top_company.click()
        sleep(2)

        # click "About"
        about_tab = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//a[text()="About"]')))
        about_tab.click()
        sleep(2)

        # Overview
        try:
            overview_element = driver.find_element(By.XPATH, '//h2[text()="Overview"]/following-sibling::p[contains(@class, "break-words white-space-pre-wrap t-black--light text-body-medium")]')
            overview = overview_element.text
        except NoSuchElementException:
            overview = ''
        # Website
        try:
            website_element = driver.find_element(By.XPATH, '//dt[text()="Website"]/following-sibling::dd/a[@class="link-without-visited-state ember-view"]')
            website = website_element.get_attribute('href') if website_element else ''
        except NoSuchElementException:
            website = ''
        # Industry
        try:
            industry_element = driver.find_element(By.XPATH, '//dt[text()="Industry"]/following-sibling::dd[@class="mb4 t-black--light text-body-medium"]')
            industry = industry_element.text
        except NoSuchElementException:
            industry = ''
        # Company size
        try:
            size_element = driver.find_element(By.XPATH, '//dt[text()="Company size"]/following-sibling::dd[contains(@class, "t-black--light text-body-medium")]')
            size = size_element.text
        except NoSuchElementException:
            size = ''
        # Location (Headquarters)
        try:
            location_element = driver.find_element(By.XPATH, '//dt[text()="Headquarters"]/following-sibling::dd[contains(@class, "mb4 t-black--light text-body-medium")]')
            location = location_element.text
        except NoSuchElementException:
            location = ''
        # Founded year (Founded)
        try:
            year_element = driver.find_element(By.XPATH, '//dt[text()="Founded"]/following-sibling::dd[contains(@class, "mb4 t-black--light text-body-medium")]')
            year = year_element.text
        except NoSuchElementException:
            year = ''

        # Append data to the result DataFrame
        new_row = {'Company':company_name, 'Industry':industry, 'Business Summary':overview, 'Year Founded':year, 'Location':location, 'Size':size, 'Website':website, 'LinkedIn URL':company_url}
        df_result = pd.concat([df_result, pd.DataFrame([new_row])], ignore_index=True)

    except Exception as e: # in case any unexpected error happens for a company search, we ignore and go to the next one
        print(f"Exception for {company_name}: {e}")  #just for debugging purpose
        new_row = {'Company':company_name, 'Industry':'', 'Business Summary':'', 'Year Founded':'', 'Location':'', 'Size':'', 'Website':'', 'LinkedIn URL':''}
        df_result = pd.concat([df_result, pd.DataFrame([new_row])], ignore_index=True)
        continue

# Save the result DataFrame to a new sheet in the same Excel file
with pd.ExcelWriter(variables.excel_file_path, engine='openpyxl') as writer:
    # Write the original sheet
    df_original.to_excel(writer, sheet_name='original', index=False)

    # Write the result sheet
    df_result.to_excel(writer, sheet_name='result', index=False)

# Close the WebDriver
print("Finished!")
driver.quit()
