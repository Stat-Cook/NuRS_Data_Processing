import pytest
from sqlalchemy.exc import OperationalError

from nurs_data_processing.sql_engine import NuRS_SQL


def test_constructor():
    """
    Test sql_engine binding.
    Uses minimal local sql engine with no password and no permissions.
    """
    engine = NuRS_SQL("mysql://pytest:@localhost").engine
    result = engine.execute("show databases;")
    result.fetchall()


def test_constructor_fail():
    """
    Test sql_engine binding.
    Test failure when user doesn't exist.
    """
    with pytest.raises(OperationalError):
        engine = NuRS_SQL("mysql://:@localhost").engine
        result = engine.execute("show databases;")
        result.fetchall()


def test_construct_from_yaml():
    engine = NuRS_SQL.from_config("config.yaml").engine
    result = engine.execute("show databases;")
    result.fetchall()
