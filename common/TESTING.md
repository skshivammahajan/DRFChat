Unit Test guide
=========

Install requirements:

    pip install -r requirements/testing.txt

## PyTest

#### Test Modules

http://doc.pytest.org/en/latest/goodpractices.html#conventions-for-python-test-discovery

#### References

- http://mathieu.agopian.info/presentations/2015_06_djangocon_europe/
- http://doc.pytest.org/en/latest/
- https://pytest-django.readthedocs.io/en/latest/
- http://pytest-cov.readthedocs.io/en/latest/

#### Config

    pytest.ini

#### Command

    pytest

## Coverage

#### References

- https://coverage.readthedocs.io/en/

#### Config

    .coveragerc

## Code Style

#### References

Flake8: http://flake8.pycqa.org/en/latest/user/index.html

PEP8 Error Codes: http://pep8.readthedocs.io/en/latest/intro.html#error-codes

Isort: http://isort.readthedocs.io/en/latest/

#### Command

    ./scripts/codestyle.bash
