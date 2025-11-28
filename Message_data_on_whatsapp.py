import pandas as pd
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Initialize WebDriver
options = Options()
options.add_argument("--remote-debugging-port=9222")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 100)
driver.maximize_window()
time.sleep(2)

# Open the URL and perform login
driver.get("https://brioanalytics.ai/")
driver.find_element(By.ID, "login-button_").click()
time.sleep(2)

username = wait.until(EC.visibility_of_element_located((By.ID, "username")))
username.send_keys("Username")

password = wait.until(EC.visibility_of_element_located((By.ID, "password")))
password.send_keys("Password")

login = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "login-button"))).click()
time.sleep(2)

client = wait.until(EC.visibility_of_element_located((By.ID, "client_select"))).send_keys(147)

element_to_click = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='mb-md-3 col-lg-3 col-md-4 col-sm-12'])[2]")))
element_to_click.click()
time.sleep(1)

submit_button = wait.until(EC.visibility_of_element_located((By.ID, "submit_searchtool_qa_2")))
submit_button.click()

show_entry = wait.until(EC.visibility_of_element_located((By.NAME, "qa-data-table-se_length")))
select = Select(show_entry)
select.select_by_visible_text("100")

clients = ["demo hair care 11:00", "demo hair care 16:00", "metro 01:00", "metro 05:00", "metro 09:00", "metro 12:00", "Richfeel", "zepto 10:00", "zepto 12:00", "zepto 14:00", "zepto 16:00", "zepto 18:00", "zepto 20:00"]

messages = []  # To store all messages

# Iterate through each client in the list
for client in clients:
    search_bar = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="search"]')))
    search_bar.clear()  # Clear the search bar before entering the next client name
    search_bar.send_keys(client)
    search_bar.send_keys(Keys.RETURN)  # Press Enter to search

    # Wait for the table and its contents to load
    show_entry = wait.until(EC.visibility_of_element_located((By.NAME, "qa-data-table-se_length")))
    select = Select(show_entry)
    select.select_by_visible_text("100")

    table = wait.until(EC.visibility_of_element_located((By.ID, 'qa-data-table-se')))
    rows = table.find_elements(By.CSS_SELECTOR, 'tr')

    # Start creating messages for this client
    print(f"\nProcessing client: {client}")  # Added newline before client
    client_message = f"Client: {client};"  # Start with the client name

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')

        if len(cells) < 10:
            continue

        website_name = cells[1].text  # Column 2 (index 1)
        product_type = cells[5].text
        status = cells[9].text

        # Format the message correctly
        client_message += f" {website_name}, {product_type}, {status};"

    # Remove trailing semicolon and append the message
    messages.append(client_message.rstrip(';'))

# Save all the messages to a text file
with open('messages.txt', 'w') as file:
    for message in messages:
        file.write(message + '\n')

print("All clients processed and messages saved to 'messages.txt'.")

driver.quit()

def whatsappLoginAndSendMessage(messages):
    # Set up Chrome options
    options = Options()
    options.add_argument("--remote-debugging-port=9222")  # Remote debugging port

    # Set up ChromeDriver service
    service = Service(ChromeDriverManager().install())

    # Initialize WebDriver
    driver = None
    try:
        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://web.whatsapp.com")
        print("Please log in to WhatsApp Web manually.")

        # Wait for the QR code to disappear (indicating login is successful)
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='New chat']"))
        )
        print("Logged in successfully. Proceeding with sending messages.")

        # Find the chat (replace contact's name or your own name)
        search_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='textbox']"))
        )
        search_box.click()
        search_box.send_keys('ME')  # Replace with your own name or contact name

        # Wait for the chat to appear and click on it
        chat = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//span[@title='Yourcontactname']"))  # Replace with your own name or contact name
        )
        chat.click()

        # Type and send the messages one by one
        message_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "(//div[@contenteditable='true' and @role='textbox'])[2]"))
        )
        for message in messages:
            message_box.click()
            message_box.send_keys(message)
            time.sleep(2)
            message_box.send_keys(Keys.RETURN)  # Send message
            time.sleep(1)

        print("Messages sent successfully.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if driver:
            driver.quit()  # Ensure browser is closed

# Call the function to send WhatsApp messages
whatsappLoginAndSendMessage(messages)
