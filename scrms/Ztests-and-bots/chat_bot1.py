from selenium import webdriver
from time import sleep
import string
import random
from random import randint

def id_generator(size=randint(3, 5), chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



user = 'SNB@mail.ru'
user_pass = 'uJ18aH9hICK'

driver = webdriver.Chrome('./chromedriver')
driver.get("http://127.0.0.1:9898")


login = driver.find_element_by_id('inputEmail').send_keys(user)
password = driver.find_element_by_id('inputPassword').send_keys(user_pass)
driver.find_element_by_id('send').click()
sleep(3)
elm = '//*[@id="scrims_chat_contact_list"]/div[1]/div[2]/div/div[1]/span'
companion = driver.find_elements_by_xpath(elm)
companion[0].click()

input_chat = driver.find_element_by_id('scrims_chat_textarea')

send = driver.find_element_by_id('scrims_chat_send')



while True:
    input_chat.send_keys(id_generator())
    sleep(1)
    send.click()
