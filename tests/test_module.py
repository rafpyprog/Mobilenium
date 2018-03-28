import os

import pytest

from mobilenium import mobidriver


BROWSER_MOB_PATH = os.path.join(os.getcwd(), 'bin', 'browsermob-proxy-2.1.4',
                                'bin', 'browsermob-proxy')

def test_mobidriver_start():
    mob = mobidriver.Firefox(BROWSER_MOB_PATH)
    assert isinstance(mob, mobidriver.Firefox)
    mob.quit()


def test_mobidriver_get_url():
    try:
        mob = mobidriver.Firefox(BROWSER_MOB_PATH)
        test_url = 'https://httpbin.org/'
        status_code = mob.get(test_url)
        assert mob.title == 'httpbin(1): HTTP Client Testing Service'
    finally:
        mob.quit()
