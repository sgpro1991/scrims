from selenium import webdriver
from time import sleep
import string
import random
from random import randint

def id_generator(size=randint(3, 100), chars=string.ascii_uppercase + string.digits):
    import random

    foo = ['battery', 'correct', 'horse', 'staple','Searching','seems','which','Daniel']
    secure_random = random.SystemRandom()
    a = []
    for i in range(0, randint(3, 100)):
        a.append(secure_random.choice(foo))
    print(a)
    return (' '.join(a))



user = '0U3@mail.ru'
user_pass = 'KGfip28mg9L'

driver = webdriver.Chrome('./chromedriver')
driver.get("http://127.0.0.1:9898")


login = driver.find_element_by_id('inputEmail').send_keys(user)
password = driver.find_element_by_id('inputPassword').send_keys(user_pass)
driver.find_element_by_id('send').click()
sleep(1)
elm = '//*[@id="scrims_chat_contact_list"]/div[1]/div[2]/div/div[1]/span'
companion = driver.find_elements_by_xpath(elm)
companion[0].click()

input_chat = driver.find_element_by_id('scrims_chat_textarea')

send = driver.find_element_by_id('scrims_chat_send')



while True:
    input_chat.send_keys(id_generator())
    sleep(1)
    send.click()
