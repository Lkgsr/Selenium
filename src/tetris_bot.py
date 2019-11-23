#!/usr/bin/python
# Author: omgimanerd (Alvin Lin)
#
# Attempts to play Tetris naively by interfacing via simple CV and keyboard
# inputs.
from selenium import webdriver

from lib.field import Field
#from optimizer import Optimizer
from lib.tetromino import Tetromino
import numpy as np
import pyautogui
import time



TETROMINO = {
    'l': Tetromino.LTetromino,
    's': Tetromino.STetromino,
    'o': Tetromino.OTetromino,
    'i': Tetromino.ITetromino,
    'j': Tetromino.JTetromino,
    't': Tetromino.TTetromino,
    'z': Tetromino.ZTetromino
}

def detect_mouse():
    print("Press enter to select mouse coordinate:")
    input()
    return pyautogui.position()

def get_pixel(coordinate):
    return pyautogui.screenshot().getpixel(coordinate)

def get_keystrokes(rotation, column, keymap):
    keys = []
    # First we orient the tetronimo
    if rotation == 1:
        keys.append(keymap['rotate_right'])
    elif rotation == 2:
        keys.append(keymap['rotate_right'])
        keys.append(keymap['rotate_right'])
    elif rotation == 3:
        keys.append(keymap['rotate_right'])
        keys.append(keymap['rotate_right'])
        keys.append(keymap['rotate_right'])
    # Then we move it all the way to the the left that we are guaranteed
    # that it is at column 0. The main reason for doing this is that when
    # the tetromino is rotated, the bottom-leftmost piece in the tetromino
    # may not be in the 3rd column due to the way Tetris rotates the piece
    # about a specific point. There are too many edge cases so instead of
    # implementing tetromino rotation on the board, it's easier to just
    # flush all the pieces to the left after orienting them.
    for i in range(4):
        keys.append(keymap['move_left'])
    # Now we can move it back to the correct column. Since pyautogui's
    # typewrite is instantaneous, we don't have to worry about the delay
    # from moving it all the way to the left.
    for i in range(column):
        keys.append(keymap['move_right'])
    keys.append(keymap['drop'])
    return keys


def get_t(rows):
    value = ""
    cols = rows[0].find_elements_by_tag_name("td")
    while value == "":
        for col in cols:
            value = col.get_attribute("class")
            if value:
                print('erstes', value)
                return TETROMINO.get(value)


def get_next_t(next_rows):
    value = ""
    cols = next_rows[0].find_elements_by_tag_name("td")
    while value == "":
        for col in cols:
            value = col.get_attribute("class")
            if value:
                print('erstes', value)
                return TETROMINO.get(value)



if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.set_window_rect(10, 10, int(1080/2), int(1920/2))
    driver.get('http://blockbattle.net/start/game')
    time.sleep(5)
    name_changer_button = driver.find_element_by_class_name('name')
    button = name_changer_button.find_element_by_id('playername_button')
    name_fild = name_changer_button.find_element_by_id('playername')
    button.click()
    name_fild.send_keys("Botti")
    button_start_game = driver.find_element_by_id('start_game')
    button_start_game.click()

    block_to_index = {
        'j': 1,
        'l': 2,
        'z': 3,
        'i': 4,
        't': 5,
        'o': 6,
        's': 7
    }
    first_rows = driver.find_element_by_xpath('//*[@id="player"]').find_elements_by_tag_name("tr")
    next_rows = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div/table/tbody').find_elements_by_tag_name("tr")
    field = Field()
    current_tetromino = get_t(first_rows)()
    print(current_tetromino)
    next_tetromino = None
    while True:
        time.sleep(1)
        try:
            next_tetromino = get_next_t(next_rows)()
        except Exception as e:
            driver.quit()
            quit()
            print(str(e))
        print(next_tetromino)
        opt = field.get_optimal_drop(current_tetromino)
        rotation = opt[-1]
        column = opt[1]
        current_tetromino.rotate(rotation)
        field.drop(current_tetromino, column)
        keys = get_keystrokes(rotation, column, {
            'rotate_right': 'k',
            'move_left': 'h',
            'move_right': 'l',
            'drop': ' '
        })
        pyautogui.typewrite(keys)
        current_tetromino = next_tetromino
        time.sleep(0.2)
