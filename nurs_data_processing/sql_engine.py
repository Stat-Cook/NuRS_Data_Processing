"""
Bindings to SQL Alchemy module
"""

import sqlalchemy
import yaml


def make_engine(sql_string):
    """
    Produce engine with 'connect_args' for project compatibility.
    Parameters
    ----------
    sql_string: str
        Connection string
    """
    return sqlalchemy.create_engine(
        sql_string,
        connect_args={'ssl': {'ssl-mode': 'preferred'}}
    )


class NuRS_SQL:

    def __init__(self, sql_string):
        self.sql_string = sql_string
        self._engine = None

    @classmethod
    def from_config(cls, config_file_path="config.yaml"):
        with open(config_file_path, "r") as f:
            config = yaml.safe_load(f)
        sql_string = config["sql_string"]
        return cls(sql_string)

    @property
    def engine(self):
        if self._engine is None:
            self._engine = make_engine(self.sql_string)

        return self._engine


def sql_engine_from_yaml(config_file_path="config.yaml"):
    """
    Produce sql alchemy engine from config file.
    """
    nurs_sql = NuRS_SQL.from_config(config_file_path)
    engine = nurs_sql.engine
    return engine
