'''
Copyright 2017 Rafael Alves Ribeiro

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''

from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from simplejson.scanner import JSONDecodeError


class Firefox(webdriver.Firefox):
    def __init__(self, browsermob_binary=None, firefox_binary=None,
                 firefox_profile=None, capabilities=None,
                 allow_insecure_certs=False, timeout=30, headless=False,
                 firefox_options=None):

        self.browsermob_binary = browsermob_binary
        self.blacklist = {}
        self.set_browsermob_proxy()
        self.add_proxy_to_profile(firefox_profile)
        self.firefox_binary = firefox_binary

        self.capabilities = capabilities
        if self.capabilities is True:
            self.allow_insecure_certs()

        self.firefox_options = Options()
        if headless is True:
            self.firefox_options.add_argument('-headless')
        if firefox_options:
            [self.firefox_options.add_argument(arg) for arg in firefox_options]

        webdriver.Firefox.__init__(self, firefox_binary=self.firefox_binary,
                                   firefox_profile=self.profile,
                                   capabilities=self.capabilities,
                                   firefox_options=self.firefox_options)

    def add_proxy_to_profile(self, profile):
        if profile is None:
            self.profile = webdriver.FirefoxProfile()
            self.profile.set_proxy(self.proxy.selenium_proxy())
        else:
            self.profile = profile
            self.profile.set_proxy(self.proxy.selenium_proxy())

    def set_browsermob_proxy(self):
        server = Server(self.browsermob_binary)
        server.start()
        self.proxy = server.create_proxy()

    def add_blacklist(self, blacklist_urls):
        '''
        Sets a list of URL patterns to blacklist

        :param blacklist_urls: dict of urls to blacklist(key) and the HTTP
               status code to return for URLs(value)

        '''
        for pattern in blacklist_urls:
            self.blacklist[pattern] = blacklist_urls[pattern]

        for url in self.blacklist:
            self.proxy.blacklist(url, self.blacklist[url])

    @property
    def har(self):
        try:
            har = self.proxy.har
        except JSONDecodeError:
            har = None
        return har

    def get(self, url):
        self.proxy.new_har(options={'captureHeaders': True})
        super(webdriver.Firefox, self).get(url)
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
