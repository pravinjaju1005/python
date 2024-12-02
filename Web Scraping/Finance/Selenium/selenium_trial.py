from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

# Open the website
driver.get("https://www.niftyindices.com/reports/historical-data")

# Wait for the first dropdown to be visible
wait = WebDriverWait(driver, 10)
try:
    # Waiting for the first dropdown to appear and selecting 'Equity' (3rd option)
    dropdown_equity = wait.until(EC.presence_of_element_located((By.ID, "ddlHistoricaltypee")))
    select_equity = Select(dropdown_equity)
    print("First dropdown found.")
    
    # Select the 3rd option (index 2) which should be 'Equity'
    select_equity.select_by_index(2)
    print("Selected 'Equity' from the first dropdown.")
    
except Exception as e:
    print(f"Error finding or selecting the first dropdown: {e}")
    driver.quit()

# Wait for the second dropdown to be populated after selecting the first one
try:
    print("Waiting for second dropdown to appear...")
    dropdown_index = wait.until(EC.presence_of_element_located((By.ID, "ddlHistoricaltypeeindex")))
    select_index = Select(dropdown_index)
    print("Second dropdown found.")

    # Now we wait for the dropdown options to be populated
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#ddlHistoricaltypeeindex option")))
    print("Second dropdown options populated.")
    
    # Get all options from the second dropdown
    options = select_index.options
    print(f"Second dropdown has {len(options)} options.")
    
    # Loop through the options and select the first one other than index 0
    for i in range(1, len(options)):
        if options[i].is_enabled():
            select_index.select_by_index(i)
            print(f"Selected option {i} from the second dropdown.")
            break
    
except Exception as e:
    print(f"Error finding or interacting with the second dropdown: {e}")
    driver.quit()

# Wait for any potential page updates after selections
try:
    print("Waiting for the page to update...")
    wait.until(EC.invisibility_of_element_located((By.ID, "loadingIndicator")))
    print("Page updated.")
    
    # Assert no "No results found" message exists on the page
    if "No results found." not in driver.page_source:
        print("Results found.")
    else:
        print("No results found.")
        
except Exception as e:
    print(f"Error during page update or results check: {e}")

# Wait a few seconds to observe the results before closing the browser
time.sleep(5)

# Close the browser
driver.quit()
