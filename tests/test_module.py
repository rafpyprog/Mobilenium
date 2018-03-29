import os
import json

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from mobilenium import mobidriver


BROWSER_MOB_PATH = os.path.join(os.getcwd(), 'bin', 'browsermob-proxy-2.1.4',
                                'bin', 'browsermob-proxy')


def test_mobidriver_start():
    try:
        mob = mobidriver.Firefox(BROWSER_MOB_PATH, headless=True)
        assert isinstance(mob, mobidriver.Firefox)
    finally:
        mob.quit()


def test_mobidriver_get_url():
    try:
        mob = mobidriver.Firefox(BROWSER_MOB_PATH, headless=True)
        test_url = 'https://httpbin.org/ip'
        status_code = mob.get(test_url)
        assert mob.title == ''
    finally:
        mob.quit()


def test_mobidriver_har():
    try:
        mob = mobidriver.Firefox(BROWSER_MOB_PATH, headless=True)
        assert mob.har is None
        test_url = 'https://httpbin.org/ip'
        mob.get(test_url)
        assert isinstance(mob.har, dict)
        assert isinstance(mob.har['log']['entries'], list)
    finally:
        mob.quit()


def test_har_is_updating():
    try:
        mob = mobidriver.Firefox(BROWSER_MOB_PATH, headless=True)

        test_url = 'http://jkorpela.fi/forms/testing.html'

        mob.get(test_url)
        WebDriverWait(mob, 2).until(EC.title_is('Testing HTML forms'))
        first_har = mob.har
        mob.find_elements_by_tag_name('input')[2].click()

        WebDriverWait(mob, 2).until(EC.title_is('Echoing submitted form data'))
        new_har = mob.har

        assert first_har != new_har
    finally:
        mob.quit()


def test_blacklist_url():
    try:
        mob = mobidriver.Firefox(BROWSER_MOB_PATH, headless=True)
        assert mob.blacklist == {}

        test_url = 'http://jkorpela.fi/forms/testing.html'
        BLACKLISTED_URL = 'http://jkorpela.fi/basic.css'
        BLACKLIST = {BLACKLISTED_URL: 404}

        mob.add_blacklist(BLACKLIST)
        mob.get(test_url)

        for entrie in mob.har['log']['entries']:
            assert entrie['request']['url'] != BLACKLISTED_URL
    finally:
        mob.quit()
