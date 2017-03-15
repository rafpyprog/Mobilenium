import os
import selenium
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import copy
from browsermobproxy import Server

import user_agent

class Mobilenium(webdriver.Firefox):
    def __init__(self, firefox_binary=None, firefox_profile=None,
                 capabilities=None, allow_insecure_certs=False, timeout=30):
        self.har = None
        self.blacklist = []
        self.set_browsermob_proxy()
        self.add_proxy_to_profile(firefox_profile)

        self.capabilities = capabilities
        if self.capabilities is True:
            self.allow_insecure_certs()

        webdriver.Firefox.__init__(self, firefox_binary=firefox_binary,
                                   firefox_profile=self.profile,
                                   capabilities=self.capabilities)

    def add_proxy_to_profile(self, profile):
        if profile is None:
            self.profile = webdriver.FirefoxProfile()
            self.profile.set_proxy(self.proxy.selenium_proxy())
        else:
            self.profile = profile
            self.profile.set_proxy(self.proxy.selenium_proxy())

    def set_browsermob_proxy(self):
        if os.name == 'posix':
            browsermob_path = "browsermob-proxy-2.1.4/bin/browsermob-proxy"
        else :
            browsermob_path = "browsermob-proxy-2.1.4/bin/browsermob-proxy.bat"
        server = Server(browsermob_path)
        server.start()
        self.proxy = server.create_proxy()

    def blacklist(self, blacklist_urls):
        '''
        Sets a list of URL patterns to blacklist

        :param blacklist_urls: dict of urls to blacklist(key) and the HTTP
               status code to return for URLs(value)

        '''
        blacklist_urls = {}
        for url in blacklist_urls:
            self.proxy.blacklist(url, blacklist[url])

    def get(self, url):
        self.proxy.new_har(options={'captureHeaders': True})
        super(webdriver.Firefox, self).get(url)
        self.har = self.proxy.har
        return self.status_code

    def allow_insecure_certs(self):
        if self.capabilities is None:
            self.capabilities = DesiredCapabilities.FIREFOX.copy()

        self.capabilities['acceptInsecureCerts'] = True

    @property
    def request(self):
        if self.har is not None:
            return self.har['log']['entries'][0]['request']
        else:
            return None

    @property
    def response(self):
        if self.har is not None:
            return self.har['log']['entries'][0]['response']
        else:
            return None

    @property
    def headers(self):
        if self.response is not None:
            headers = {}
            for header_field in self.response['headers']:
                headers[header_field['name']] = header_field['value']
            return headers
        else:
            return None

    @property
    def status_code(self):
        ''' Integer Code of responded HTTP Status, e.g. 404 or 200. '''
        if self.response is not None:
            return self.response['status']
        else:
            return None