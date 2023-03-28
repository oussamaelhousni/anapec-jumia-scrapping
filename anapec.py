from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from time import sleep
driver = webdriver.Chrome()
base_url = "http://anapec.org/sigec-app-rv/"
driver.get(base_url)

radio_emp = driver.find_element(By.CSS_SELECTOR,"input#radio_1")
email_element = driver.find_element(By.CSS_SELECTOR,"input#user")
password_element = driver.find_element(By.CSS_SELECTOR,"input#pass")
ok_button = driver.find_element(By.CSS_SELECTOR,"input.btn_connexion.pull-right")
radio_emp.click()
email = "email"
password = "*******"

email_element.send_keys(email)
password_element.send_keys(password)
ok_button.click()

try:
    modal = driver.find_element(By.CSS_SELECTOR,"#myModal")
    close_btn = modal.find_element(By.CSS_SELECTOR,".modal-header > .close")
    close_btn.click()
except:
    print("no modal poped up")

dataframe = pd.DataFrame({
    "ref contrat":[],
    "date signatute":[],
    "date fin":[],
    "etat anapec":[],
    "type":[],
    "modele":[],
    "cin":[],
    "traitement cnss":[]
})
for i in range(1,3):
    driver.get(f"http://anapec.org/sigec-app-rv/fr/entreprises/visualiser_contrat/page:{i}")
    table = driver.find_element(By.CSS_SELECTOR,"table")
    rows = table.find_elements(By.CSS_SELECTOR,"tbody > tr")
    for j in range(0,len(rows)):
        columns = rows[j].find_elements(By.CSS_SELECTOR,"td")
        dataframe = pd.concat([pd.DataFrame([[columns[0].text,columns[1].text,columns[2].text,columns[3].text,columns[4].text,columns[5].text,columns[6].text,columns[7].text]], columns=dataframe.columns), dataframe], ignore_index=True)

dataframe.to_excel("anapec.xls")

"""
    new_row = {
    "ref contrat":"",
    "date signatute":"",
    "date fin":"",
    "etat anapec":"",
    "type":"",
    "modele":"",
    "cin":"",
    "traitement cnss":""
    }
"""