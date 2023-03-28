from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import re
from pymongo import MongoClient
driver = webdriver.Chrome()

# jumia official website
jumia_base_url = "https://www.jumia.ma/ar"

# catgeories that we want
products = {
    "maison-cuisine-jardin":[],
    "ordinateurs-accessoires-informatique":[],
    "sports-loisirs":[]
}

## close popup's
def close_button(page_url,driver):
    driver.get(page_url)
    try:
        close_btn = driver.find_element(By.CSS_SELECTOR, '.cls[aria-label="newsletter_popup_close-cta"]')
        close_btn.click()
    except:
        print("no pop up's")
        
## get products of a specific category
def get_products(category):
    global products
    products_elements = driver.find_elements(By.CSS_SELECTOR,".-paxs.row._no-g._4cl-3cm-shs .prd._fb.col.c-prd")
    for product in products_elements:
        product_info = {}
        product_info["title"] = ""
        if len(product.find_elements(By.CSS_SELECTOR,".info h3.name")) > 0 :
            product_info["title"] = product.find_elements(By.CSS_SELECTOR,".info h3.name")[0].text
        
        product_info["url"] = ""
        if len(product.find_elements(By.CSS_SELECTOR,".core")) > 0 :
            product_info["url"] = product.find_elements(By.CSS_SELECTOR,".core")[0].get_attribute("href")
        
        product_info["image"] = ""
        if len(product.find_elements(By.CSS_SELECTOR,".img-c img")) > 0:
            product_info["image"] = product.find_elements(By.CSS_SELECTOR,".core .img-c > img")[0].get_attribute("data-src")
            
        price_element = ""
        if len(product.find_elements(By.CSS_SELECTOR,".info .prc")) > 0:
            price_element = product.find_elements(By.CSS_SELECTOR,".info .prc")[0].text
        
        old_price_element = ""
        if len(product.find_elements(By.CSS_SELECTOR,".s-prc-w .old")) > 0:
            old_price_element = product.find_elements(By.CSS_SELECTOR,".s-prc-w .old")[0].text
            
        product_info["current_price"] = current_price = float(re.findall(r'[\d]*[.][\d]+',price_element)[0]) if price_element != "" else 0
        product_info["old_price"] = old_price = float(re.findall(r'[\d]*[.][\d]+',old_price_element)[0]) if old_price_element != "" else 0
        discount = 0
        if old_price > 0 and current_price > 0 and current_price < old_price:
            product_info["discount_percentage"] = round(100 - (current_price / old_price )*100)
            product_info["discount_quantity"]  = round(old_price - current_price)
        products[category].append(product_info)
        
# wanted categories
categories = ["maison-cuisine-jardin","ordinateurs-accessoires-informatique","sports-loisirs"]

for category in categories:
    category_url = f"{jumia_base_url}/{category}"
    for page in range(1,3):
        page_url = f"{category_url}/?page={str(page)}"
        close_button(page_url,driver)
        get_products(category)
        
#### save the data to mongoDB
client = MongoClient()
client = MongoClient('localhost', 27017)
# scrap database
db = client.scrap
def save(products):
    for category,items in products.items():
        try:
            db[category].delete_many({})
            db[category].insert_many(items)
        except:
            print("error")

save(products)