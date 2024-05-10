# content of unit_test.py

import re


def pytest_generate_tests(metafunc):
    # вызывается один раз для каждой тестовой функции
    funcarglist = metafunc.cls.params[metafunc.function.__name__]
    argnames = sorted(funcarglist[0])
    metafunc.parametrize(
        argnames, [[funcargs[name] for name in argnames] for funcargs in funcarglist]
    )


class TestUrlShame:
    params = {
        "test_valid_url_scheme": [
            dict(url="http://www.example.com"),
            dict(url="https://www.example.com"),
            dict(url="ftp://ftp.example.com")
        ],
        "test_invalid_url_no_scheme": [
            dict(url="www.example.com"),
            dict(url="example.com"),
            dict(url="localhost:8080/page")
        ]
    }

    def test_valid_url_scheme(self, url):
        pattern = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://")
        assert re.match(pattern, url)

    def test_invalid_url_no_scheme(self, url):
        pattern = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://")
        assert not re.match(pattern, url)

class TestUrlNetloc:
    params = {
        "test_valid_url_netloc": [
            dict(url="http://www.example.com"),
            dict(url="https://subdomain.example.com/page"),
            dict(url="ftp://ftp.example.com")
        ],
        "test_invalid_url_no_netloc": [
            dict(url="http://"),
            dict(url="https://"),
            dict(url="ftp://")
        ]
    }

    def test_valid_url_netloc(self, url):
        pattern = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://[^\s/$.?#].[^\s]*$")
        assert re.match(pattern, url)

    def test_invalid_url_no_netloc(self, url):
        pattern = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://[^\s/$.?#].[^\s]*$")
        assert not re.match(pattern, url)


class TestUrlPath:
    params = {
        "test_valid_url_path": [
            dict(url="http://example.com/path"),
            dict(url="http://example.com/path/to/resource")
        ],
        "test_invalid_url_path": [
            dict(url="http://example.com"),
            dict(url="https://example.com")
        ]
    }

    def test_valid_url_path(self, url):
        pattern = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://([a-zA-Z0-9-._~%!$&'()*+,;=:]*)?(/[a-zA-Z0-9-._~%!$&'()*+,;=:@]*)+")
        assert re.match(pattern, url)

    def test_invalid_url_path(self, url):
        pattern = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://([a-zA-Z0-9-._~%!$&'()*+,;=:]*)?(/[a-zA-Z0-9-._~%!$&'()*+,;=:@]*)+")
        assert not re.match(pattern, url)


class TestUrlQuery:
    params = {
        "test_valid_url_query": [
            dict(url="http://example.com/page?param=value"),
            dict(url="http://example.com/path?query=123&test=true")
        ]
    }

    def test_valid_url_query(self, url):
        assert "?" in url


class TestUrlFragment:
    params = {
        "test_valid_url_fragment": [
            dict(url="http://example.com/page#section1"),
            dict(url="http://example.com/page#section2")
        ]
    }

    def test_valid_url_fragment(self, url):
        assert "#" in url