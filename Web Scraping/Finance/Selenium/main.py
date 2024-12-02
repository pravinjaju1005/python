from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

# Set up the WebDriver (ensure you have the appropriate driver for your browser)
driver = webdriver.Chrome()  # Update the path

try:
    # Navigate to the Nifty Indices Reports page
    driver.get('https://www.niftyindices.com/reports')

    # Wait for the page to load
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "HistoricalMenu")))

    # First dropdown (Historical Index Data)
    historical_menu = driver.find_element(By.ID, "HistoricalMenu")
    print(f"First Dropdown Label: {historical_menu.text}")

    # Second dropdown (Index Type)
    index_type_dropdown = Select(driver.find_element(By.ID, "ddlHistoricaltypee"))
    print("Second Dropdown Options:")
    for option in index_type_dropdown.options:
        print(option.text)

    # Select an option from the second dropdown (e.g., "Equity")
    index_type_dropdown.select_by_visible_text("Equity")
    print(f"Selected Index Type: {index_type_dropdown.first_selected_option.text}")

    # Wait for the third dropdown to become available
    WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.ID, "ddlHistoricaltypeeindex")))

    # Third dropdown (Historical Type Index)
    index_dropdown = Select(driver.find_element(By.ID, "ddlHistoricaltypeeindex"))
    print("Third Dropdown Options:")
    for option in index_dropdown.options:
        print(option.text)

    # Select an option from the third dropdown (e.g., "NIFTY 50")
    index_dropdown.select_by_visible_text("NIFTY 50")
    print(f"Selected Index: {index_dropdown.first_selected_option.text}")

finally:
    # Wait before closing the browser (for demonstration purposes)
    time.sleep(5)
    driver.quit()
