Mobilenium: Selenium with steroids
==================================

Mobilenium uses [Browsermob Proxy](https://github.com/AutomatedTester/browsermob-proxy-py) to give superpowers to Selenium.

Usage
------------

    >>> from mobilenium import Mobilenium
    >>>
    >>> mob = Mobilenium()
    >>> mob.get("http://python-requests.org")
    301
    >>> mob.response['redirectURL']
    'http://docs.python-requests.org'
    >>> mob.headers["Content-Type"]
    'application/json; charset=utf8'
    >>> mob.title
    'Requests: HTTP for Humans \u2014 Requests 2.13.0 documentation'
    >>> mob.find_elements_by_tag_name("strong")[1].text
    'Behold, the power of Requests'

Mobilenium allows you to use Selenium and have access to status codes and HTTP headers, without the need for manual labor. It is powered by Browsermob Proxy, which is embedded within Mobilenium.

Installation
------------
    git clone https://rafael_ribeiro_dev@bitbucket.org/rafael_ribeiro_dev/mobilenium.git

Contribute
------------
Contributions are welcome! Not familiar with the codebase yet? No problem! There are many ways to contribute to open source projects: reporting bugs, helping with the documentation, spreading the word and of course, adding new features and patches.
