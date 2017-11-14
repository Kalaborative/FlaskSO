from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import requests
import pytest
from flask import get_flashed_messages

driver = webdriver.Chrome()
non_number_in_ID = "Please submit a valid ID. Numbers only!"
invalid_length = "Invalid length. Try again."

def test_setup():
	driver.get('localhost:5000')
	driver.implicitly_wait(30)
	title = driver.find_element_by_id('title-text').text
	assert "Welcome" in title

def test_flash_1():
	driver.find_element_by_tag_name('input').send_keys('dlfkdjd')
	driver.find_element_by_id('login-button').click()
	message = driver.find_element_by_tag_name('p')
	assert message.text == non_number_in_ID

def test_flash_2():
	driver.find_element_by_tag_name('input').send_keys('3092')
	driver.find_element_by_id('login-button').click()
	message = driver.find_element_by_tag_name('p')
	assert message.text == invalid_length

def test_flash_3():
	driver.find_element_by_tag_name('input').send_keys('302233a')
	driver.find_element_by_id('login-button').click()
	message = driver.find_element_by_tag_name('p')
	assert message.text == non_number_in_ID

def test_flash_4():
	driver.find_element_by_tag_name('input').send_keys('Mangohero1')
	driver.find_element_by_id('login-button').click()
	messages = driver.find_elements_by_tag_name('p')
	assert messages[0].text == non_number_in_ID
	assert messages[1].text == invalid_length

def test_account():
	driver.find_element_by_tag_name('input').send_keys('2030020')
	driver.find_element_by_id('login-button').click()
	cards = driver.find_elements_by_tag_name('li')
	assert len(cards) == 1

def result():
	driver.get('localhost:5000/results/4835124/Mom')
	title = driver.find_element_by_tag_name('h1').text

def test_result():
	with pytest.raises(NoSuchElementException):
		result()


def test_code():
	driver.get('http://localhost:5000/randomstuff')
	status_code = driver.find_element_by_tag_name('h1').text
	assert "Not Found" in status_code

def test_special_char():
	driver.get('localhost:5000')
	driver.find_element_by_tag_name('input').send_keys('000-000')
	driver.find_element_by_id('login-button').click()
	message = driver.find_element_by_tag_name('p')
	assert message.text == non_number_in_ID

def test_teardown():
	called = []
	driver.quit()
	called.append(True)
	assert len(called) == 1
