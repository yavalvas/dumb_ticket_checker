#! -*- coding: utf-8 -*-
import time, threading
import sys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import pygame

import time


driver = webdriver.Chrome(executable_path="./chromedriver.exe")


def login_user(login, password):
    driver.delete_all_cookies()
    # driver.get('http://rezerwacja.duw.pl/reservation/pol/queues/38/27')
    driver.get('http://rezerwacja.duw.pl/reservation/pol/login')
    driver.find_element_by_id("UserEmail").send_keys(login)
    driver.find_element_by_id("UserPassword").send_keys(password)
    driver.find_element_by_xpath("//input[@value='Zaloguj']").click()
    driver.find_element_by_xpath("//*[contains(text(), 'rezerwacje w 2017 roku')]").click()
    driver.find_element_by_xpath(
        "//*[contains(text(), 'złożenie wniosku o legalizację pobytu/residence permit 2017')]").click()
    return driver


no_tickets_message = "Przepraszamy, brak wolnych biletów "


def validate_tickets(month_name, all_elements):
    for ticket in all_elements:
        ticket.click()
        print("{} Day {}".format(month_name, ticket.get_attribute('innerHTML')))
        time.sleep(0.1)
        try:
            driver.find_element_by_xpath("//*[contains(text(), '{}')]".format(no_tickets_message))
            print("No ticket")
        except NoSuchElementException:
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(open("ticket_found.wav", "rb"))
            pygame.mixer.music.play()
            # sound = pygame.mixer.Sound("ticket_found.wav")
            # sound.play()
            while pygame.mixer.music.get_busy():
                time.sleep(1)
            print("Take ticket!!!")
            # driver.quit()
            print("Ticket is found for {} {}".format(month_name, ticket.get_attribute('innerHTML')))
            time.sleep(300)
            # sys.exit("Ticket is found for {} {}".format(month_name, ticket.get_attribute('innerHTML')))


def check(driver):
    print(time.ctime())
    all_elements = driver.find_elements_by_xpath("//div[@class='day good']")
    validate_tickets("April", all_elements)
    # driver.find_element_by_id('zabuto_calendar_1k9d_nav-next').click()
    nav_right = driver.find_elements_by_xpath("//div[@class='calendar-month-navigation']")[1]
    nav_right.click()
    all_elements = driver.find_elements_by_xpath("//div[@class='day good']")
    validate_tickets("May", all_elements)
    # driver.find_element_by_id('zabuto_calendar_1k9d_nav-prev').click()
    nav_left = driver.find_elements_by_xpath("//div[@class='calendar-month-navigation']")[0]
    nav_left.click()
    threading.Timer(1, lambda: check(driver)).start()


driver = login_user(login="***", password="***")
check(driver)