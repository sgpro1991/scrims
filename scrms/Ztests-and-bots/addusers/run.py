from selenium import webdriver
from time import sleep
import os
import string
import random
from random import randint

def id_generator(size=randint(3, 5), chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

user = 'sgpro1991'
user_pass = 'q1w2e3r4'

driver = webdriver.Chrome('../chromedriver')
driver.get("http://127.0.0.1:9898/admin/users/user/add/")


login = driver.find_element_by_id('id_username').send_keys(user)
password = driver.find_element_by_id('id_password').send_keys(user_pass)

driver.find_elements_by_xpath('//*[@id="login-form"]/div[3]/input')[0].click()



path = "/home/sgpro1991/scrims_enviroment/scrims/scrms/Ztests-and-bots/addusers/img/"
images = os.listdir(path)

print(images)


for a in images:
    name = a.replace('.jpg','').replace('.png','').replace('.jpeg','')
    mail = id_generator()+'@mail.ru'
    driver.find_elements_by_id('id_image')[0].send_keys(path+a)
    driver.find_elements_by_id('id_name')[0].send_keys(name)
    driver.find_elements_by_id('id_email')[0].send_keys(mail)
    driver.find_elements_by_id('id_position')[0].send_keys('1')
    driver.find_elements_by_xpath('//*[@id="user_form"]/div/div/input[2]')[0].click()
    sleep(1)
