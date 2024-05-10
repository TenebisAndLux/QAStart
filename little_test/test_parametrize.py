# content of ./test_parametrize.py
import re
import pytest

def pytest_generate_tests(metafunc):  # called once for each target function
    funcarglist = metafunc.cls.params[metafunc.function.__name__]
    argnames = sorted(funcarglist[0])
    metafunc.parametrize(argnames, [[funcargs[name] for name in argnames] for funcargs in funcarglist])


class TestURLs:
    params = {
        "test_valid_url_scheme": [
            dict(url="http://www.example.com"),
            dict(url="https://www.example.com"),
            dict(url="ftp://ftp.example.com")
        ],
        "test_valid_url_netloc": [
            dict(url="http://www.example.com"),
            dict(url="https://subdomain.example.com/page"),
            dict(url="ftp://ftp.example.com")
        ],
        "test_invalid_url_no_scheme": [
            dict(url="www.example.com"),
            dict(url="example.com"),
            dict(url="localhost:8080/page")
        ],
        "test_invalid_url_no_netloc": [
            dict(url="http://"),
            dict(url="https://"),
            dict(url="ftp://")
        ],
        "test_invalid_url_no_scheme_netloc": [
            dict(url="www example com"),
            dict(url="example"),
            dict(url="http:")
        ]
    }

    def test_valid_url_scheme(self, url):
        pattern = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
        assert re.match(pattern, url)

    def test_valid_url_netloc(self, url):
        pattern = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://[^\s/$.?#].[^\s]*$")
        assert re.match(pattern, url)

    def test_invalid_url_no_scheme(self, url):
        pattern = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://")
        assert not re.match(pattern, url)

    def test_invalid_url_no_netloc(self, url):
        pattern = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://[^\s/$.?#].[^\s]*$")
        assert not re.match(pattern, url)

    def test_invalid_url_no_scheme_netloc(self, url):
        pattern = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://[^\s/$.?#].[^\s]*$")
        assert not re.match(pattern, url)
