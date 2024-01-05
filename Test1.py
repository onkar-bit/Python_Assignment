from selenium import webdriver
import json
import time
import pytest
from selenium.webdriver.common.by import By


# URL of the test page
url = "https://testpages.herokuapp.com/styled/tag/dynamic-table.html"

# Sample data to insert and assert
sample_data = [
    {"name": "Bob", "age": 20, "gender": "male"},
    {"name": "George", "age": 42, "gender": "male"},
    {"name": "Sara", "age": 42, "gender": "female"},
    {"name": "Conor", "age": 40, "gender": "male"},
    {"name": "Jennifer", "age": 42, "gender": "female"}
]

# Create a JSON string from the sample data
json_data = json.dumps(sample_data)

# Initialize the WebDriver (assuming you have chromedriver in your PATH)

@pytest.fixture(scope="module", params=None, autouse=False, ids=None, name=None)
def setup_driver():
    driver = webdriver.Firefox(executable_path='/automatepyth/newbuy/geckodriver.exe')
    driver.maximize_window()
    yield driver
    driver.close()

    # Step 1: Open the URL
def test_DynamicTable(setup_driver):

    driver = setup_driver
    driver.get(url)

    # Step 2: Click on Table Data button
    table_data_button = driver.find_element(By.XPATH, "//summary[text()='Table Data']")
    table_data_button.click()

    # Step 3: Insert data and click on Refresh Table button
    input_textbox = driver.find_element(By.XPATH, "//textarea[@id='jsondata']")
    input_textbox.clear()
    input_textbox.send_keys(json_data)

    refresh_table_button = driver.find_element(By.XPATH, "//button[@id='refreshtable']")
    refresh_table_button.click()

    # Give some time for the table to be refreshed
    time.sleep(2)

    # Step 4: Assert the data in the table
    table_rows = driver.find_elements(By.XPATH, "//table[@id='dynamictable']//tr")

    # Skip the header row if present (assuming the first row is a header)
    for index, row in enumerate(table_rows[1:], start=0):
        # Check if there's corresponding data in sample_data
        if index < len(sample_data):
            columns = row.find_elements(By.TAG_NAME, "td")

            # Check if the number of columns matches the length of sample_data
            if len(columns) != len(sample_data[index]):
                pytest.fail(f"Error: Number of columns in row {index} does not match the length of sample_data.")

            assert columns[0].text == sample_data[index]["name"]
            assert int(columns[1].text) == sample_data[index]["age"]
            assert columns[2].text == sample_data[index]["gender"]
        else:
            pytest.fail(f"Error: No corresponding data in sample_data for row {index}.")

    print("Assertion Passed: Data in the table matches the provided data.")

    # Close the browser window
    #driver.quit()
