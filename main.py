import time, sched
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from pprint import pprint

driver_path = "C:/Users/nicol/Documents/Development/chromedriver.exe"
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

driver.get("http://orteil.dashnet.org/experiments/cookie/")
five_min_timeout = time.time() + 60 * 5  # 5 minutes from now
purchase_list = {}

cookie = driver.find_element(By.XPATH, '//*[@id="cookie"]')

i = 0
while True:
    money = int(driver.find_element(By.ID, 'money').text.replace(",", ""))

    for n in range(100):
        cookie.click()

    if i % 5 == 0:
        print("Every 5 seconds")
        purchase_options = driver.find_elements(By.CSS_SELECTOR, '#store b')

        for i in range(len(purchase_options)):
            try:
                name = purchase_options[i].text.split()[0:-2]
                price = purchase_options[i].text.split()[-1].replace(',', '')
            except IndexError:
                continue
            else:
                purchase_list[i] = {"price": int(price), "name": " ".join(name)}

        for k, v in reversed(sorted(list(purchase_list.items()))):
            if money > v["price"]:
                buy = driver.find_element(By.ID, f"buy{v['name']}")
                buy.click()
                print(f"Bought {v['name']} which cost {v['price']}")
                break

    if time.time() > five_min_timeout:
        cookies_per_seconds = driver.find_element(By.ID, "cps").text
        print(cookies_per_seconds)
        driver.quit()
        break

    i += 1
    time.sleep(1)