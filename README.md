
# LinkedIn Company Data Scraper

This project is a time-saving solution for gathering and organizing information about companies. It automatically navigates LinkedIn and extracts data like company size, location, website and more. Perfect for gaining insights into numerous companies quickly, this tool does the heavy lifting, saving time and energy compared to manual searches.

## Info it extracts

- Company Name
- Industry
- Business Summary
- Year Founded
- Location
- Size
- Website
- LinkedIn URL


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`LINKEDIN_USERNAME`

`LINKEDIN_PASSWORD`


## Installation & Setup
* Download the project into your local computer  
* In VS Code, open the project folder  
* [Create a virtual environment](https://code.visualstudio.com/docs/python/environments#_creating-environments)
* Download dependencies
  ```bash
  pip install pandas
  ```
  ```bash
  pip install -r requirements.txt
  ```
* In "variables.py", upate the following paths:  
  a. `chrome_driver_path`  
  - update it to the path of the "chromedriver.exe" in your project folder
  - In case the chromedriver does not work, you can always download it again from "https://googlechromelabs.github.io/chrome-for-testing/"
    
  b. `excel_file_path`  
  - update it to the path of your excel source file  
  - make sure in your source file, the list of companies are located under the header "Company"
  

## Run Locally

* Before running, make sure your source file is closed (otherwise you'll get "permission denied" error)
* In "main.py", click "Run Without Debugging"
* A LinkedIn page will pop up, it will login using the username and password from .env
* If LinkedIn asks for security check, do it manually
* Maximize the LinkedIn screen while the script is running, it will speed up the process
