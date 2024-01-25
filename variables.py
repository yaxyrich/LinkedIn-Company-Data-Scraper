from dotenv import load_dotenv
import os

load_dotenv()

my_username = os.environ['LINKEDIN_USERNAME']
my_password = os.environ['LINKEDIN_PASSWORD']

# Your chromedriver location goes here:
chrome_driver_path = r"C:\Users\ylin\OneDrive - Fiera Capital Corporation\Desktop\project\chromedriver.exe"

# Your excel file path goes here:
excel_file_path = r"C:\Users\ylin\OneDrive - Fiera Capital Corporation\Desktop\project\tester.xlsx"
