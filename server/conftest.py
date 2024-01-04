import pytest


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """启用django数据库连接: https://pytest-django.readthedocs.io/en/latest/faq.html#how-can-i-make-sure-that-all-my-tests-run-with-a-specific-locale

    方式有几种，这是其中一种，更多信息请参阅: https://pytest-django.readthedocs.io/en/latest/database.html
    """
    pass
