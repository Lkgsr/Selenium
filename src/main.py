from selenium import webdriver
import numpy as np
from PIL import ImageGrab
import os
import cv2
import time


driver = webdriver.Firefox()
driver.get('http://blockbattle.net/start/game')
time.sleep(5)
name_changer_button = driver.find_element_by_class_name('name')
button = name_changer_button.find_element_by_id('playername_button')
name_fild = name_changer_button.find_element_by_id('playername')
button.click()
name_fild.send_keys("Botti")

button_start_game = driver.find_element_by_id('start_game')
button_start_game.click()

all_classes = []

block_to_index = {
    'j': 1,
    'l': 2,
    'z': 3,
    'i': 4,
    't': 5,
    'o': 6,
    's': 7
}

for x in range(20):
    rows = driver.find_element_by_xpath('//*[@id="player"]').find_elements_by_tag_name("tr")
    screen = []
    for index_, row in enumerate(rows):
        cols = row.find_elements_by_tag_name("td")
        new_row = np.zeros(len(cols))
        for index, col in enumerate(cols):
            value = col.get_attribute("class")
            if value:
                if value not in all_classes:
                    all_classes.append(value)
                new_row[index] = block_to_index.get(value)
        screen.append(new_row)
    game_data = np.array(screen)

    # flip horizontally to make our final fix in visual representation:
    #flipped = cv2.flip(game_data, 0)
    resized = cv2.resize(game_data, dsize=None, fx=10, fy=10)

    cv2.imshow('Intel', resized)
    cv2.waitKey(1)
    #time.sleep(1/60)





#print(all_classes)
time.sleep(5)

driver.quit()